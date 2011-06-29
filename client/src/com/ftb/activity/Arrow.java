package com.ftb.activity;

import android.content.Context;
import android.graphics.*;
import android.view.View;
import android.widget.ImageView;
import com.ftb.R;

public class Arrow extends ImageView{
    Paint paint;
  float direction = 0;

  public Arrow(Context context) {
    super(context);

    paint = new Paint();
    paint.setColor(Color.WHITE);
    paint.setStrokeWidth(2);
    paint.setStyle(Paint.Style.STROKE);
    this.setImageResource(R.drawable.arrow_left);

  }

  @Override
  public void onDraw(Canvas canvas) {
    int height = this.getHeight();
    int width = this.getWidth();
//
//      canvas.drawLine(150, 250, 300, 250, paint);
//      canvas.drawLine(300,250,275,225,paint);
//      canvas.drawLine(300,250,275,275,paint);
//
//      ImageView image = new ImageView(getContext());
//      image.setImageResource(R.drawable.arrow_big);
//      Bitmap bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.arrow_big);
//      canvas.drawBitmap(bitmap,150,250,paint);


      canvas.rotate(direction, width / 2, height / 2);
    super.onDraw(canvas);
  }

  public void setDirection(float direction) {
    this.direction = direction;
    this.invalidate();
  }
}
