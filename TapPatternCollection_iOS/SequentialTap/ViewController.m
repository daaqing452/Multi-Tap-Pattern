//
//  ViewController.m
//  SequentialTap
//
//  Created by Yiqin Lu on 2019/6/19.
//  Copyright © 2019 Yiqin Lu. All rights reserved.
//

#import "ViewController.h"
#import <AVFoundation/AVFoundation.h>
#import <CoreMotion/CoreMotion.h>

@interface ViewController ()

@property (weak, nonatomic) IBOutlet UIButton *buttonLog;
@property (weak, nonatomic) IBOutlet UIButton *buttonDelete;
@property (weak, nonatomic) IBOutlet UIButton *buttonCalibration;
@property (weak, nonatomic) IBOutlet UILabel *labelTimestamp;

@end

@implementation ViewController

// general
NSFileManager *fileManager;
NSString *documentPath;

// inertial
bool const SENSOR_SHOW_DETAIL = false;
CMMotionManager *motionManager;
double prevMotionTimestamp;

// microphone
AVAudioRecorder *recorder;

- (void)viewDidLoad {
    [super viewDidLoad];
    
    fileManager = [NSFileManager defaultManager];
    documentPath = [NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES) objectAtIndex:0];
    
    motionManager = [[CMMotionManager alloc] init];
    [self setInertialDataGetPush];
    
    /*[[AVAudioSession sharedInstance] setCategory:AVAudioSessionCategoryPlayAndRecord withOptions:AVAudioSessionCategoryOptionDefaultToSpeaker | AVAudioSessionCategoryOptionMixWithOthers | AVAudioSessionCategoryOptionAllowBluetooth error:nil];
    NSURL *url = [NSURL fileURLWithPath:@"/dev/null"];
    NSDictionary *settings = [NSDictionary dictionaryWithObjectsAndKeys: [NSNumber numberWithFloat: 44100.0], AVSampleRateKey, [NSNumber numberWithInt: kAudioFormatAppleLossless], AVFormatIDKey, [NSNumber numberWithInt: 2], AVNumberOfChannelsKey, [NSNumber numberWithInt: AVAudioQualityMax], AVEncoderAudioQualityKey, nil];
    NSError *error;
    recorder = [[AVAudioRecorder alloc] initWithURL:url settings:settings error:&error];*/
    
    self.view.multipleTouchEnabled = TRUE;
    NSLog(@"force %@", self.traitCollection.forceTouchCapability == UIForceTouchCapabilityAvailable ? @"enabled" : @"disabled");
}



// log
int const LOG_BUFFER_MAX_SIZE = 16384;
bool const LOG_SHOW_FILE_SIZE = false;
bool logging = false;
NSString *buffer = @"";
NSString *logFileName;

- (IBAction)doClickButtonLog:(id)sender {
    if (logging) {
        [self writeFile:logFileName content:buffer];
        buffer = @"";
        [self.buttonLog setTitle:@"Log: Off" forState:UIControlStateNormal];
        logging = false;
    } else {
        [self.buttonLog setTitle:@"Log: On" forState:UIControlStateNormal];
        NSString *timeString = [self getTimeString:@"YYYYMMdd-HHmmss"];
        logFileName = [NSString stringWithFormat:@"touch-%@.txt", timeString];
        logging = true;
    }
}

- (IBAction)doClickButtonDelete:(id)sender {
    [self deleteFiles:documentPath];
}

- (IBAction)doClickCalibration:(id)sender {
    [self.labelTimestamp setText:[NSString stringWithFormat:@"%lf", prevMotionTimestamp]];
}



/*
 * sensor
 */
- (void)setInertialDataGetPush {
    if (!motionManager.deviceMotionAvailable) return;
    motionManager.deviceMotionUpdateInterval = 1/100.0;
    __block int freqCnt = 0;
    NSDate *startTime = [NSDate date];
    [motionManager startDeviceMotionUpdatesToQueue:[NSOperationQueue mainQueue] withHandler:^(CMDeviceMotion * _Nullable motion, NSError * _Nullable error) {
        if (error) return;
        freqCnt++;
        prevMotionTimestamp = motion.timestamp;
        CMAcceleration acceleration = motion.userAcceleration;
        CMRotationRate rotationRate = motion.rotationRate;
        CMAttitude *attitude = motion.attitude;
        if (SENSOR_SHOW_DETAIL) {
            float freq = freqCnt / (-[startTime timeIntervalSinceNow]);
            NSLog(@"acc %f %f %f", acceleration.x, acceleration.y, acceleration.z);
            NSLog(@"freqAcc: %f", freq);
        }
//        if (logging) {
//            buffer = [buffer stringByAppendingString:[NSString stringWithFormat:@"time %f\nacc %f %f %f\nrot %f %f %f\natt %f %f %f\n", motion.timestamp, acceleration.x, acceleration.y, acceleration.z, rotationRate.x, rotationRate.y, rotationRate.z, attitude.roll, attitude.pitch, attitude.yaw]];
//            if (buffer.length > LOG_BUFFER_MAX_SIZE) {
//                [self writeFile:logFileName content:buffer];
//                buffer = @"";
//            }
//        }
    }];
    NSLog(@"push motion ready");
}



/*
 * touch
 */
int currentTouchNumber = 0;

-(void)touchesBegan:(NSSet*)touches withEvent:(UIEvent*)event {
    @synchronized (self) {
        for (UITouch *touch in touches) {
            CGPoint point = [touch locationInView:[touch view]];
            if (logging) {
                [self writeFile:logFileName content:[NSString stringWithFormat:@"%f down %f %f\n", touch.timestamp, point.x, point.y]];
            }
            //NSLog(@"%f %f", point.x, point.y);
        }
        currentTouchNumber += touches.count;
        NSLog(@"down %d (%lu)", currentTouchNumber, touches.count);
    }
}

-(void)touchesMoved:(NSSet*)touches withEvent:(UIEvent*)event {
//    for (UITouch *touch in touches) {
//        NSLog(@"force %f", touch.force);
//    }
}

-(void)touchesEnded:(NSSet*)touches withEvent:(UIEvent*)event {
    @synchronized (self) {
        for (UITouch *touch in touches) {
            CGPoint point = [touch locationInView:[touch view]];
            if (logging) {
                [self writeFile:logFileName content:[NSString stringWithFormat:@"%f up %f %f\n", touch.timestamp, point.x, point.y]];
            }
            //NSLog(@"%f %f", point.x, point.y);
        }
        currentTouchNumber -= touches.count;
        NSLog(@"up %d", currentTouchNumber);
    }
}

-(void)touchesCancelled:(NSSet*)touches withEvent:(UIEvent*)event {
    // interupt by other event, such as a call
}



/*
 * file
 */
- (void)writeFile:(NSString *)fileName content:(NSString *)content {
    NSString *filePath = [documentPath stringByAppendingPathComponent:fileName];
    NSFileHandle *fileHandle = [NSFileHandle fileHandleForWritingAtPath:filePath];
    if (fileHandle == nil) {
        NSError *error;
        bool ifSuccess = [content writeToFile:filePath atomically:YES encoding:NSUTF8StringEncoding error:&error];
        NSLog(@"write file %@: %@", ifSuccess ? @"Yes" : @"No", ifSuccess ? fileName : error);
    } else {
        [fileHandle truncateFileAtOffset:[fileHandle seekToEndOfFile]];
        [fileHandle writeData:[content dataUsingEncoding:NSUTF8StringEncoding]];
        [fileHandle closeFile];
        if (LOG_SHOW_FILE_SIZE) {
            long long size = [[fileManager attributesOfItemAtPath:filePath error:nil] fileSize];
            NSLog(@"writing size: %lld", size);
        }
    }
}

- (NSString *)getTimeString:(NSString *)format {
    NSDateFormatter *formatter = [[NSDateFormatter alloc] init];
    [formatter setDateFormat:format];
    NSDate *now = [NSDate date];
    return [formatter stringFromDate:now];
}

- (void)deleteFiles:(NSString *)path {
    NSDirectoryEnumerator *myDirectoryEnumerator = [fileManager enumeratorAtPath:path];
    NSString *file;
    while ((file = [myDirectoryEnumerator nextObject])) {
        NSString *filePath = [documentPath stringByAppendingPathComponent:file];
        bool ifSuccess = [fileManager removeItemAtPath:filePath error:nil];
        NSLog(@"delete file %@: %@", ifSuccess ? @"Yes" : @"No", file);
    }
}

@end
