package com.ftb.activity;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

import java.io.ObjectInputStream;

public class SensorLogic  implements SensorEventListener {
  private float[] mMagneticValues;
  private float[] mAccelerometerValues;

  private float mAzimuth;

  @Override
  public void onAccuracyChanged(Sensor sensor, int accuracy) {
  }

  @Override
  public void onSensorChanged(SensorEvent event) {
    synchronized (this) {
      switch (event.sensor.getType()) {
      case Sensor.TYPE_MAGNETIC_FIELD:
        mMagneticValues = event.values.clone();
        break;
      case Sensor.TYPE_ACCELEROMETER:
        mAccelerometerValues = event.values.clone();
        break;
      }

      if (mMagneticValues != null && mAccelerometerValues != null) {
        float[] R = new float[9];
        SensorManager.getRotationMatrix(R, null, mAccelerometerValues, mMagneticValues);
        float[] orientation = new float[3];
        SensorManager.getOrientation(R, orientation);
        mAzimuth = orientation[0];
      }
    }
  }

    public float getAzimuth(){
        return mAzimuth;
    }
}
