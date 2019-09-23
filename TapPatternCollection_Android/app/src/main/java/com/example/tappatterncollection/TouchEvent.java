package com.example.tappatterncollection;

import android.app.Activity;

import java.util.ArrayList;

public class TouchEvent {

    MainActivity activity;
    ArrayList<Point> p;

    public TouchEvent(MainActivity activity, int x, int y, long t) {
        this.activity = activity;
        p = new ArrayList();
        p.add(new Point(x, y, t % this.activity.T_MOD));
    }

    public void move(int x, int y, long t) {
        p.add(new Point(x, y, t % this.activity.T_MOD));
    }

    public Point first() {
        if (p.size() == 0) return null;
        return p.get(0);
    }

    public Point last() {
        if (p.size() == 0) return null;
        return p.get(p.size() - 1);
    }
}

class Point {
    int x, y;
    long t;
    public Point(int x, int y, long t) {
        this.x = x;
        this.y = y;
        this.t = t;
    }
}