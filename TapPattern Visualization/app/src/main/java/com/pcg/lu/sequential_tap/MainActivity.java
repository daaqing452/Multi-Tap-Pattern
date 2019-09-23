package com.pcg.lu.sequential_tap;

import android.support.constraint.ConstraintLayout;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;

import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;


public class MainActivity extends AppCompatActivity {

    public final static int VIEW_SEQUENTIAL = 0;
    public final static int VIEW_GESTURE = 1;

    DrawView drawView;
    int page = VIEW_SEQUENTIAL;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        onChangeView(VIEW_SEQUENTIAL);
    }

    void onChangeView(int target) {
        page = target;
        switch (page) {
            case VIEW_SEQUENTIAL:
                setContentView(R.layout.sequential_tap);
                ConstraintLayout layout = findViewById(R.id.main_layout);
                drawView = new DrawView(this);
                //drawView.setBackgroundColor(Color.BLACK);
                //drawView.setAlpha(0.5f);
                layout.addView(drawView);
                break;
            case VIEW_GESTURE:
                setContentView(R.layout.gesture);
                break;
        }
    }

    TouchEvent[] touchEvent = new TouchEvent[10];
    ArrayList<QTouch> qtouchs = new ArrayList();
    Timer idleTimer = null;

    public boolean onTouchEvent(MotionEvent event) {
        //return super.onTouchEvent(event);

        int n = event.getPointerCount();
        int index = event.getActionIndex();
        int pointerID = event.getPointerId(index);
        int x = (int)event.getX(index);
        int y = (int)event.getY(index);
        //Log.d("pressure", event.getPressure(index) + "");

        switch (event.getActionMasked()){
            case MotionEvent.ACTION_DOWN:
            case MotionEvent.ACTION_POINTER_DOWN:
                touchEvent[pointerID] = new TouchEvent(this, x, y);
                if (idleTimer != null) {
                    idleTimer.cancel();
                    idleTimer = null;
                }
                break;

            case MotionEvent.ACTION_MOVE:
                touchEvent[pointerID].move(x, y);
                break;

            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_POINTER_UP:
                TouchEvent touch = touchEvent[pointerID];
                touch.up(x, y);
                switch (page) {
                    case VIEW_SEQUENTIAL:
                        qtouchs.add(new QTouch((touch.x+touch.downX)/2, (touch.y+touch.downY)/2, touch.downTime, touch.currentTime));
                        if (n - 1 == 0) {
                            idleTimer = new Timer();
                            idleTimer.schedule(new IdleTimerTask(), 200);
                        }
                        break;
                }
                touchEvent[pointerID] = null;
                break;
        }
        return super.onTouchEvent(event);
    }

    class IdleTimerTask extends TimerTask {
        public void run() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                QTouch.sequentialize(qtouchs);
                drawView.drawIntervel(qtouchs);
                qtouchs = new ArrayList();
                }
            });
        }
    }

    public void buttonPageOnChange(View v) {
        switch (page) {
            case VIEW_SEQUENTIAL:
                onChangeView(VIEW_GESTURE);
                break;
            case VIEW_GESTURE:
                onChangeView(VIEW_SEQUENTIAL);
                break;
        }
    }
}
