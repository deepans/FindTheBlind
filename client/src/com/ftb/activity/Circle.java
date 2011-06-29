package com.ftb.activity;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.view.View;

public class Circle extends View{
    private float x = 150;
    private float y = 250;
    private int r= 150;
    private Paint mPaint = new Paint(Paint.ANTI_ALIAS_FLAG);

    public Circle(Context context) {
        super(context);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        canvas.drawCircle(x,y,r,mPaint);
    }
}
