package com.pcg.lu.sequential_tap;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.util.Log;
import android.view.View;

import java.util.ArrayList;

class DrawView extends View {
    final static int DEVICE_WIDTH = 1440;
    final static int DEVICE_HEIGHT = 2960;

    Bitmap bitmap = null;
    Canvas canvas = null;

    public DrawView(Context context) {
        super(context);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (bitmap != null) canvas.drawBitmap(bitmap, 0, 0, new Paint());
    }

    void drawIntervel(ArrayList<QTouch> qtouchs) {
        bitmap = Bitmap.createBitmap(DEVICE_WIDTH, DEVICE_HEIGHT, Bitmap.Config.ARGB_8888);
        canvas = new Canvas(bitmap);

        Paint p_red = new Paint();
        p_red.setColor(Color.RED);
        p_red.setStrokeWidth(10);

        Paint p_blue = new Paint();
        p_blue.setColor(Color.BLUE);

        for (int i = 0; i < qtouchs.size(); i++) {
            QTouch qtouch = qtouchs.get(i);
            int y = (qtouch.order + 1) * 100;
            canvas.drawLine(qtouch.l * 1000f + 100f, y, qtouch.r * 1000 + 100, y, p_red);
            canvas.drawCircle(qtouch.x, qtouch.y - 250, 10, p_blue);
        }

        invalidate();
    }
}