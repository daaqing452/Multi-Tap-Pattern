//
//  InterfaceController.m
//  TapPattern-demo WatchKit Extension
//
//  Created by 鲁逸沁 on 2019/7/22.
//  Copyright © 2019 Yiqin Lu. All rights reserved.
//

#import "InterfaceController.h"
#import <Foundation/Foundation.h>
#import <HealthKit/HealthKit.h>
#import <CoreMotion/CoreMotion.h>
#import <WatchConnectivity/WatchConnectivity.h>

@interface InterfaceController () <WCSessionDelegate, HKWorkoutSessionDelegate>

@property (weak, nonatomic) IBOutlet WKInterfaceLabel *labelInfo;
@property (weak, nonatomic) IBOutlet WKInterfaceButton *buttonLog;


@property (strong, nonatomic) CMMotionManager *motionManager;
@property (strong, nonatomic) HKWorkoutConfiguration *workoutConfiguration;
@property (strong, nonatomic) HKHealthStore *healthScore;
@property (strong, nonatomic) HKWorkoutSession *workoutSession;

@end


@implementation InterfaceController

WKInterfaceDevice *device;
WCSession *wcsession;
bool logging = false;

- (void)awakeWithContext:(id)context {
    [super awakeWithContext:context];
    if ([WCSession isSupported]) {
        wcsession = [WCSession defaultSession];
        wcsession.delegate = self;
        [wcsession activateSession];
    }
}

- (void)willActivate {
    [super willActivate];
    
    // workout
    self.workoutConfiguration = [[HKWorkoutConfiguration alloc] init];
    self.workoutConfiguration.activityType = HKWorkoutActivityTypeRunning;
    self.workoutConfiguration.locationType = HKWorkoutSessionLocationTypeOutdoor;
    self.healthScore = [[HKHealthStore alloc] init];
    self.workoutSession = [[HKWorkoutSession alloc] initWithHealthStore:self.healthScore configuration:self.workoutConfiguration error:nil];
    [self.workoutSession startActivityWithDate:[NSDate date]];
    
    // general
    device = [WKInterfaceDevice currentDevice];
    self.motionManager = [[CMMotionManager alloc] init];
    [self setSensorDataGetPush];
    NSLog(@"init finished");
}

- (void)didDeactivate {
    [super didDeactivate];
}

- (void)parseCommand:(NSString *)command {
    if ([command isEqualToString:@"log on"]) {
        [self changeLogStatus:true];
    } else if ([command isEqualToString:@"log off"]) {
        [self changeLogStatus:false];
    } else {
        NSLog(@"recv: %@", command);
    }
}

- (void)changeLogStatus:(bool)status {
    if (status == true) {
        [self.buttonLog setTitle:@"Log On"];
        logging = true;
    } else {
        [self.buttonLog setTitle:@"Log Off"];
        logging = false;
    }
}



//
//  --- UI ---
//
- (IBAction)doClickButtonLog:(id)sender {
    [self changeLogStatus:!logging];
}



//
//  --- sensor ---
//
const int N_FARR = 60;
float farr[N_FARR];
int fi = 0;

- (void)transit:(float *)nowData length:(int)length {
    for (int i = 0; i < length; i++) {
        farr[fi++] = nowData[i];
    }
    if (fi >= N_FARR) {
        char *carr = (char *)farr;
        NSData *data = [NSData dataWithBytes:carr length:N_FARR * sizeof(float)];
        [self sendData:@{@"message": @"data", @"data": data}];
        fi = 0;
    }
}

- (void)setSensorDataGetPush {
    if (!self.motionManager.deviceMotionAvailable) return;
    self.motionManager.deviceMotionUpdateInterval = 1/100.0;
    
    // push
    [self.motionManager startDeviceMotionUpdatesToQueue:[NSOperationQueue mainQueue] withHandler:^(CMDeviceMotion * _Nullable motion, NSError * _Nullable error) {
        if (error) return;
        CMAcceleration acceleration = motion.userAcceleration;
        CMRotationRate rotationRate = motion.rotationRate;
        float nowData[6] = {(float)acceleration.x, (float)acceleration.y, (float)acceleration.z, (float)rotationRate.x, (float)rotationRate.y, (float)rotationRate.z};
        if (logging) {
            [self transit:nowData length:6];
        }
    }];
    NSLog(@"push motion ready");
}



//
//  --- watch connectivity ---
//
- (void)sendData:(NSDictionary *)dict {
    [wcsession sendMessage:dict replyHandler:^(NSDictionary<NSString *,id> * _Nonnull replyMessage) {
        // ignore
    } errorHandler:^(NSError * _Nonnull error) {
        // error
    }];
}

- (void)sendMessage:(NSString *)message {
    [self sendData:@{@"message": message}];
}

- (void)session:(nonnull WCSession *)session didReceiveMessage:(nonnull NSDictionary<NSString *,id> *)dict replyHandler:(nonnull void (^)(NSDictionary<NSString *,id> * __nonnull))replyHandler {
    [self parseCommand:dict[@"message"]];
}

- (void)session:(nonnull WCSession *)session activationDidCompleteWithState:(WCSessionActivationState)activationState error:(nullable NSError *)error {
}

- (void)sendFile:(NSString *)filePath {
    NSLog(@"send file: %@", filePath);
    NSURL *fileUrl = [NSURL fileURLWithPath:filePath];
    [wcsession transferFile:fileUrl metadata:nil];
}



//
//  workout
//
- (void)workoutSession:(nonnull HKWorkoutSession *)workoutSession didChangeToState:(HKWorkoutSessionState)toState fromState:(HKWorkoutSessionState)fromState date:(nonnull NSDate *)date {
}

- (void)workoutSession:(nonnull HKWorkoutSession *)workoutSession didFailWithError:(nonnull NSError *)error {
}

- (void)workoutSession:(HKWorkoutSession *)workoutSession didGenerateEvent:(HKWorkoutEvent *)event {
}

@end



