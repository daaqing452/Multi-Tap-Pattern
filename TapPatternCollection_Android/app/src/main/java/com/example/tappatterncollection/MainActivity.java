package com.example.tappatterncollection;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Environment;
import android.os.Vibrator;
import android.util.Log;
import android.view.MotionEvent;
import android.view.SoundEffectConstants;
import android.view.View;
import android.widget.Button;
import android.widget.RadioGroup;
import android.widget.TextView;

import java.io.FileOutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;

public class MainActivity extends AppCompatActivity {
    public final int T_MOD = 100000000;

    Button buttonLog, buttonYes, buttonNo, buttonMark;
    RadioGroup radioGroupLog;
    TextView textLog;

    PrintWriter logger;
    boolean logging;
    String logType = "tap";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textLog = findViewById(R.id.textLog);
        logging = false;

        buttonLog = findViewById(R.id.buttonLog);
        buttonLog.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (logging) {
                    if (logger != null) logger.close();
                    logger = null;
                    radioGroupLog.setEnabled(true);
                    for (int i = 0; i < radioGroupLog.getChildCount(); i++) radioGroupLog.getChildAt(i).setEnabled(true);
                    textLog.setText("Off");
                    textLog.setTextColor(Color.rgb( 0, 0, 0));
                    logging = false;
                } else {
                    String filename = "touch-" + (new SimpleDateFormat("yyMMdd-hhmmss").format(new Date())) + ".txt";
                    try {
                        logger = new PrintWriter(new OutputStreamWriter(new FileOutputStream(Environment.getExternalStorageDirectory().getPath() + "/" + filename, true)), true);
                        logger.write("start " + (System.currentTimeMillis() % T_MOD) + "\n");
                        for (int i = 0; i < radioGroupLog.getChildCount(); i++) radioGroupLog.getChildAt(i).setEnabled(false);
                        textLog.setText("On");
                        textLog.setTextColor(Color.rgb( 255, 0, 0));
                        logging = true;
                    } catch (Exception e) {
                        Log.d("tappc", e.toString());
                    }
                }
            }
        });

        buttonYes = findViewById(R.id.buttonYes);
        buttonYes.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (logging) {
                    buttonYes.playSoundEffect(SoundEffectConstants.CLICK);
                    logger.write("yes " + (System.currentTimeMillis() % T_MOD) +  "\n");
                }
            }
        });

        buttonNo = findViewById(R.id.buttonNo);
        buttonNo.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (logging) {
                    logger.write("no " + (System.currentTimeMillis() % T_MOD) + "\n");
                }
            }
        });

        buttonMark = findViewById(R.id.buttonMark);
        buttonMark.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (logging) {
                    logger.write("mark " + (System.currentTimeMillis() % T_MOD) + "\n");
                }
            }
        });

        radioGroupLog = findViewById(R.id.radioGroupLog);
        radioGroupLog.setOnCheckedChangeListener(new RadioGroup.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(RadioGroup radioGroup, int i) {
                switch (i) {
                    case R.id.radioTap:
                        logType = "tap";
                        break;
                    case R.id.radioGesture:
                        logType = "gesture";
                        break;
                }
            }
        });
    }

    TouchEvent[] touchEvent = new TouchEvent[10];

    public boolean onTouchEvent(MotionEvent event){
        //if (logging == false) return super.onTouchEvent(event);
        int n = event.getPointerCount();
        int index = event.getActionIndex();
        int pointerID = event.getPointerId(index);
        int x = (int)event.getX(index);
        int y = (int)event.getY(index);
        long t = System.currentTimeMillis();

        switch (event.getActionMasked()){
            case MotionEvent.ACTION_DOWN:
            case MotionEvent.ACTION_POINTER_DOWN:
                touchEvent[pointerID] = new TouchEvent(this, x, y, t);
                break;

            case MotionEvent.ACTION_MOVE:
                for (int i = 0; i < n; i++) {
                    int j = event.getPointerId(i);
                    int xx = (int)event.getX(i);
                    int yy = (int)event.getY(i);
                    if (touchEvent[j] != null) touchEvent[j].move(xx, yy, t);
                }
                break;

            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_POINTER_UP:
                TouchEvent g = touchEvent[pointerID];
                if (g == null) break;
                g.move(x, y, t);
                Point p0 = g.first();
                Point p1 = g.last();
                if (logging) {
                    if (logType.equals("tap")) {
                        logger.write("tap " + p0.t + " " + p0.x + " " + p0.y + " " + p1.t + " " + p1.x + " " + p1.y + "\n");
                    } else {
                        logger.write("down\n");
                        for (int i = 0; i < g.p.size(); i++) {
                            Point p2 = g.p.get(i);
                            logger.write("ges " + p2.t + " " + p2.x + " " + p2.y + "\n");
                        }
                        logger.write("up\n");
                    }
                }
                Log.d("tappc", p0.t + ":(" + p0.x + "," + p0.y + ") " + p1.t + ":(" + p1.x + "," + p1.y + ")");
                touchEvent[pointerID] = null;
                break;
        }
        return super.onTouchEvent(event);
    }
}
