package com.ftb.activity;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.view.Display;
import android.view.Surface;
import android.view.WindowManager;

public class SensorLogic  implements SensorEventListener {
	
	private float[] mMagneticValues;
	private float[] mAccelerometerValues;

	float[] orientation = new float[9];
	private final LocationActivity locationActivity;

	public SensorLogic(LocationActivity locationActivity) {
		this.locationActivity = locationActivity;
	}

	@Override
	public void onAccuracyChanged(Sensor sensor, int accuracy) {
	}

	@Override
	public void onSensorChanged(SensorEvent event) {

		// If the sensor data is unreliable return
		if (event.accuracy == SensorManager.SENSOR_STATUS_UNRELIABLE) {
			return;
		}

		synchronized (this) {
			switch (event.sensor.getType()) {
			case Sensor.TYPE_MAGNETIC_FIELD:
				mMagneticValues = event.values.clone();
				break;
			case Sensor.TYPE_ACCELEROMETER:
				mAccelerometerValues = event.values.clone();
				break;
			default: return;
			}
			float[] remapedRotationM = new float[9];
			if (mMagneticValues != null && mAccelerometerValues != null) {
				float[] R = new float[9];
				// Computes the inclination matrix I as well as the rotation matrix R transforming a vector from the device coordinate system to the world's coordinate system which is defined as a direct orthonormal basis, where:
                // X is defined as the vector product Y.Z (It is tangential to the ground at the device's current location and roughly points East).
				boolean b = SensorManager.getRotationMatrix(R, null, mAccelerometerValues,
						mMagneticValues);
				
				Display display = ((WindowManager) this.locationActivity.getSystemService(Context.WINDOW_SERVICE)).getDefaultDisplay();
				int rotation = display.getOrientation();

				if (b) {
					switch (rotation) {
					case Surface.ROTATION_0:
					case Surface.ROTATION_180:
						SensorManager.remapCoordinateSystem(R,
								SensorManager.AXIS_MINUS_X,
								SensorManager.AXIS_Y, remapedRotationM);
						break;
					case Surface.ROTATION_90:
					case Surface.ROTATION_270:
						SensorManager.remapCoordinateSystem(R,
								SensorManager.AXIS_X, SensorManager.AXIS_Z,
								remapedRotationM);
						break;
					}
				}		        
				 /*SensorManager.remapCoordinateSystem(R,
						 SensorManager.AXIS_X, SensorManager.AXIS_Y, 
						 remapedRotationM);*/
								
				SensorManager.getOrientation(remapedRotationM, orientation);
				this.locationActivity.updateCompass(orientation);
			}
		}
	}

	public float getAzimuth() {
		return orientation[0];
	}
}