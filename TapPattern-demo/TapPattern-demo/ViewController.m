//
//  ViewController.m
//  TapPattern-demo
//
//  Created by 鲁逸沁 on 2019/7/22.
//  Copyright © 2019 Yiqin Lu. All rights reserved.
//

#import "ViewController.h"
#import <WatchConnectivity/WatchConnectivity.h>

#define UILog(format, ...) [self showInfoInUI:[NSString stringWithFormat:(format), ##__VA_ARGS__]]


@interface ViewController () <WCSessionDelegate>

@property (weak, nonatomic) IBOutlet UIButton *buttonLogOn;
@property (weak, nonatomic) IBOutlet UIButton *buttonLogOff;
@property (weak, nonatomic) IBOutlet UIButton *buttonClear;
@property (weak, nonatomic) IBOutlet UITextView *textView;


@end

@implementation ViewController

WCSession *wcsession;
NSFileManager *fileManager;
NSString *documentPath;

- (void)viewDidLoad {
    [super viewDidLoad];
    
    if ([WCSession isSupported]) {
        wcsession = [WCSession defaultSession];
        wcsession.delegate = self;
        [wcsession activateSession];
    }
    
    fileManager = [NSFileManager defaultManager];
    documentPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    
    [self loadSamples];
    UILog(@"init finished");
}

- (void)parseCommand:(NSString *)command {
    if ([command isEqualToString:@"test"]) {
        
    } else {
        UILog(@"recv: %@", command);
    }
}

- (void)showInfoInUI:(NSString *)newInfo {
    dispatch_async(dispatch_get_main_queue(),^{
        NSString *s = [self.textView text];
        s = [s stringByAppendingString:newInfo];
        s = [s stringByAppendingString:@"\n\n"];
        [self.textView setText:s];
    });
}



//
//  --- recognition ---
//
const int   WINDOW = 60;
const int   FRAME_PER_TRANSMIT = 10;
const float DETECT_ACC = 0.09;
const int   SIGMENT_LEN = 25;

NSBundle *bundle;
float sample[999][2][WINDOW][3];
int n_sample, sampleLabel[999];
float nowSignalAccX, prevSignalAccX;

float f[2][WINDOW * 3][3];
float rf[2][WINDOW][3];
int fi = 0;

float dp[WINDOW][WINDOW];

- (void)loadSamples {
    bundle = [NSBundle bundleWithPath:[[NSBundle mainBundle] pathForResource:@"MakeBundle" ofType:@"bundle"]];
    NSString *filePath = [bundle pathForResource:@"plain" ofType:@"txt"];
    NSData *data = [fileManager contentsAtPath:filePath];
    NSString *s = [[NSString alloc] initWithData:data encoding:NSUTF8StringEncoding];
    NSArray<NSString *> *linearr = [s componentsSeparatedByString:@"\n"];
    NSArray<NSString *> *sarr = [linearr[0] componentsSeparatedByString:@" "];
    n_sample = [sarr[0] intValue];
    sarr = [linearr[1] componentsSeparatedByString:@" "];
    int cnt = 0;
    for (int i = 0; i < n_sample; i++)
        for (int j = 0; j < 6; j++)
            for (int k = 0; k < WINDOW; k++)
                sample[i][j / 3][k][j % 3] = [sarr[cnt++] floatValue];
    sarr = [linearr[2] componentsSeparatedByString:@" "];
    for (int i = 0; i < n_sample; i++)
        sampleLabel[i] = [sarr[i] intValue];
    UILog(@"load samples: %@", filePath);
}

- (void)work:(NSData *)data {
    // retrive
    int length = (int)data.length / sizeof(float);
    float *farr = (float *)[data bytes];
    for (int i = 0; i < length; i += 6) {
        for (int j = 0; j < 2; j++)
            for (int k = 0; k < 3; k++)
                f[j][fi][k] = farr[i + j * 3 + k];
        fi++;
    }
    // shift
    if (fi >= WINDOW * 3) {
        for (int i = 0; i < WINDOW * 2; i++)
            for (int j = 0; j < 2; j++)
                for (int k = 0; k < 3; k++)
                    f[j][i][k] = f[j][i + WINDOW][k];
        fi -= WINDOW;
    }
    
    // get signal and align
    int first = -1, last = -1000;
    int sigl = -1, sigr = -1;
    for (int i = MAX(0, fi - WINDOW * 2); i < fi; i++) {
        float maxAcc = 0;
        for (int j = 0; j < 3; j++) maxAcc = MAX(maxAcc, ABS(f[0][i][j]));
        if (maxAcc > DETECT_ACC) {
            // renew non-zero signal interval
            if (i - last > SIGMENT_LEN) first = i;
            last = i;
        } else {
            if (i - last < SIGMENT_LEN || first == -1) continue;
            // signal end
            int mid = (first + last) / 2;
            if (last - first < 5) {
                NSLog(@"interval too small: (%d, %d)", first, last);
                first = -1;
                continue;
            }
            int l = mid - WINDOW / 2;
            int r = mid + WINDOW / 2;
            if (l < MAX(0, fi - WINDOW * 2) || r > fi) {
                NSLog(@"incomplete signal: (%d, %d) -> [%d, %d] in {%d, %d}", first, last, l, r, MAX(0, fi - WINDOW * 2), fi);
                first = -1;
                continue;
            }
            sigl = l;
            sigr = r;
            nowSignalAccX = f[0][mid][0];
            first = -1;
        }
    }
    
    if (sigl == -1) return;
    // remove duplication
    if (nowSignalAccX != prevSignalAccX) {
        for (int i = 0; i < WINDOW; i++)
            for (int j = 0; j < 2; j++)
                for (int k = 0; k < 3; k++)
                    rf[j][i][k] = f[j][sigl + i][k];
        [self recognition];
    }
    prevSignalAccX = nowSignalAccX;
}

- (void)recognition {
     float bestScore = 1e20;
     int bestLabel = -1;
     for (int i = 0; i < n_sample; i++) {
         if (sampleLabel[i] == 6 || sampleLabel[i] == 7) continue;
         float scoreAcc = [self DTW:0 sid:i];
         float scoreGyr = [self DTW:1 sid:i];
         float score = scoreAcc + scoreGyr;
         if (score < bestScore) {
             bestScore = score;
             bestLabel = sampleLabel[i];
         }
     }
     NSString *labels[] = {@"2", @"22", @"(23)", @"(23)(23)", @"(2345)", @"(2345)(2345)", @"k", @"kk", @"23", @"32", @"25", @"52", @"234", @"432", @"232", @"323"};
     UILog(@"ans: %@ %f", labels[bestLabel], bestScore);
 }

- (float)DTW:(int)p sid:(int)sid {
    memset(dp, 0, sizeof(dp));
    for (int i = 0; i < WINDOW; i++)
        for (int j = 0; j < WINDOW; j++) {
            float d = 1e20;
            if (i > 0) d = MIN(d, dp[i - 1][j]);
            if (j > 0) d = MIN(d, dp[i][j - 1]);
            if (i > 0 && j > 0) d = MIN(d, dp[i - 1][j - 1]);
            if (i == 0 && j == 0) d = 0;
            dp[i][j] = d + [self DTWDist:p sid:sid i:i j:j];
        }
    return dp[WINDOW - 1][WINDOW - 1];
}

- (float)DTWDist:(int)p sid:(int)sid i:(int)i j:(int)j {
    float d = 0;
    for (int k = 0; k < 3; k++) d += ABS(rf[p][i][k] - sample[sid][p][j][k]);
    return d;
}



//
//  --- UI ---
//
- (IBAction)doClickButtonLogOn:(id)sender {
    [self sendMessage:@"log on"];
}

- (IBAction)doClickButtonLogOff:(id)sender {
    [self sendMessage:@"log off"];
}

- (IBAction)doClickButtonClear:(id)sender {
    [self.textView setText:@""];
}



//
//  --- watch connectivity ---
//
- (void)sendData:(NSDictionary *)dict {
    [wcsession sendMessage:dict replyHandler:^(NSDictionary<NSString *,id> * _Nonnull replyMessage) {
        // no reply?
    } errorHandler:^(NSError * _Nonnull error) {
        UILog(@"send error %ld: %@", error.code, error);
    }];
}

- (void)sendMessage:(NSString *)message {
    [self sendData:@{@"message": message}];
}

- (void)session:(nonnull WCSession *)session didReceiveMessage:(nonnull NSDictionary<NSString *,id> *)dict replyHandler:(nonnull void (^)(NSDictionary<NSString *,id> * __nonnull))replyHandler {
    //replyHandler(@{@"message": @"yes"});
    NSString *message = dict[@"message"];
    if ([message isEqualToString:@"data"]) {
        [self work:dict[@"data"]];
    } else {
        [self parseCommand:message];
    }
}

@end
