package com.pcg.lu.sequential_tap;

import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;

import android.app.Activity;
import android.content.Context;
import android.os.Vibrator;
import android.util.Log;

public class TouchEvent {

    // parameters
    final int DRAG_TIME = 300;
    final int DWELL_DIST = 50;
    final int SWIPE_DIST = 90;

    // touch event types
    public final static int EVENT_NULL = 0;
    public final static int EVENT_CLICK = 1;
    public final static int EVENT_DRAG = 2;
    public final static int EVENT_SWIPE_LEFT = 3;
    public final static int EVENT_SWIPE_RIGHT = 4;
    public final static int EVENT_SWIPE_UP = 5;
    public final static int EVENT_SWIPE_DOWN = 6;
    public final static int EVENT_DWELL = 7;
    public final static int EVENT_RUB = 8;

    // variables
    int x, y, downX, downY;
    long downTime, currentTime;
    Activity activity;
    Timer timer;
    boolean drag = false;
    double maxDist = 0;

    public TouchEvent(Activity activity, int downX, int downY) {
        // basic
        this.activity = activity;
        this.x = this.downX = downX;
        this.y = this.downY = downY;

        // set up drag timer
        timer = new Timer();
        timer.schedule(new TouchEventTimerTask(this), DRAG_TIME);

        // count down time
        currentTime = downTime = new Date().getTime();
    }

    public void move(int x, int y) {
        // if same, ignore
        if (this.x == x && this.y == y) return;

        // update basic
        this.x = x;
        this.y = y;
        currentTime = new Date().getTime();

        // update max dist
        double nowDist = Point.dist(x, y, downX, downY);
        if (nowDist > maxDist) {
            maxDist = nowDist;
        }
    }

    public int up(int x, int y) {
        // cancel drag timer
        timer.cancel();

        // update basic
        this.x = x;
        this.y = y;
        currentTime = new Date().getTime();

        // drag or dwell
        if (drag) {
            return (maxDist < DWELL_DIST) ? EVENT_DWELL : EVENT_DRAG;
        }

        // rub?
        //if (maxDist > RUB_DIST_1 && Point.dist(x, y, maxX, maxY) > RUB_DIST_2) return EVENT_RUB;

        // click
        if (ifDwell()) {
            return EVENT_CLICK;
        }

        // swipe
        if (Math.abs(x - downX) > Math.abs(y - downY)) {
            if (x < downX - SWIPE_DIST) return EVENT_SWIPE_LEFT;
            if (x > downX + SWIPE_DIST) return EVENT_SWIPE_RIGHT;
        } else {
            if (y < downY - SWIPE_DIST) return EVENT_SWIPE_UP;
            if (y > downY + SWIPE_DIST) return EVENT_SWIPE_DOWN;
        }

        // cannot distinguish
        return EVENT_NULL;
    }

    // if dwell, compare current x/y and down x/y
    public boolean ifDwell() {
        return Point.dist(x,  y, downX, downY) < DWELL_DIST;
    }


    // drag timer
    class TouchEventTimerTask extends TimerTask {

        TouchEvent father;

        public TouchEventTimerTask(TouchEvent father) {
            this.father = father;
        }

        public void run() {
            //if (!father.ifDwell()) return;

            father.drag = true;

            /*Vibrator vibrator =  (Vibrator)father.activity.getSystemService(Context.VIBRATOR_SERVICE);
            long[] pattern = {0, 20};
            vibrator.vibrate(pattern, -1);*/
        }
    }
}


class Point {

    int x, y;
    Date date;

    public Point() {
        x = y = 0;
    }

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
        this.date = new Date();
    }

    static double dist(int x, int y, int xx, int yy) {
        return Math.sqrt(Math.pow(x - xx, 2) + Math.pow(y - yy, 2));
    }
}