package com.pcg.lu.sequential_tap;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Map;
import java.util.TreeMap;

class QTouch {
    public final static int SAME_FINGER_THRESHOLD = 150;

    public int x, y;
    public long t0, t1;
    public float l, r;
    public int index, order;

    public QTouch(int x, int y, long t0, long t1) {
        this.x = x;
        this.y = y;
        this.t0 = t0;
        this.t1 = t1;
    }

    public static void sequentialize(ArrayList<QTouch> qtouchs) {
        // normalize
        long minT = Long.MAX_VALUE;
        long maxT = Long.MIN_VALUE;
        for (int i = 0; i < qtouchs.size(); i++) {
            QTouch qtouch = qtouchs.get(i);
            minT = Math.min(minT, qtouch.t0);
            maxT = Math.max(maxT, qtouch.t1);
        }
        for (int i = 0; i < qtouchs.size(); i++) {
            QTouch qtouch = qtouchs.get(i);
            qtouch.l = 1.0f * (qtouch.t0 - minT) / (maxT - minT);
            qtouch.r = 1.0f * (qtouch.t1 - minT) / (maxT - minT);
        }

        // find same finger
        for (int i = 0; i < qtouchs.size(); i++) {
            QTouch qti = qtouchs.get(i);
            qti.index = i;
            for (int j = 0; j < i; j++) {
                QTouch qtj = qtouchs.get(j);
                if (Point.dist(qti.x, qti.y, qtj.x, qtj.y) < SAME_FINGER_THRESHOLD) {
                    qti.index = qtj.index;
                    break;
                }
            }
        }

        // order
        TreeMap<Integer, QTouch> map = new TreeMap();
        for (int i = 0; i < qtouchs.size(); i++) {
            QTouch qtouch = qtouchs.get(i);
            if (qtouch.index == i) {
                map.put(qtouch.x, qtouch);
            }
        }
        Iterator iter = map.entrySet().iterator();
        int order = 0;
        while (iter.hasNext()) {
            Map.Entry entry = (Map.Entry)iter.next();
            QTouch qtouch = (QTouch)entry.getValue();
            qtouch.order = order++;
        }
        for (int i = 0; i < qtouchs.size(); i++) {
            QTouch qtouch = qtouchs.get(i);
            if (qtouch.index != i) {
                qtouch.order = qtouchs.get(qtouch.index).order;
            }
        }
    }
}