package com.ftb.activity;

import android.app.Activity;
import android.content.Intent;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.hardware.GeomagneticField;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.ftb.R;

public class LocationActivity extends Activity {

	private SensorManager sensorManager;
	private SensorLogic sensorEventListener;
	private Arrow arrow;
	private LocationManager locationManager;
	private LocationLogic locationListener = new LocationLogic();

	private TextView distance;
	private TextView allValues;
	
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.location);
		LinearLayout layout = (LinearLayout) findViewById(R.id.location);

		arrow = new Arrow(this);
		LinearLayout actionLayout = getActionLayout();

		layout.addView(arrow);
				
		distance = new TextView(this);
	    layout.addView(distance);

	    allValues = new TextView(this);
	    layout.addView(allValues);

	    layout.addView(actionLayout);
	    
		sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
		locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

		sensorEventListener = new SensorLogic(this);
		// float azimuth = sensorEventListener.getAzimuth();
		// Location userLocation = locationListener.getLocation();
		//
		// if(userLocation == null){
		// userLocation = getLocation(50.066389, -5.71472);
		// }
		//
		// Location patientLocation = getLocation(58.64389, -3.07);
		//
		// float[] results = new float[3];
		// Location.distanceBetween(userLocation.getLatitude(),
		// userLocation.getLongitude(),patientLocation.getLatitude(),patientLocation.getLongitude(),
		// results);
		//
		// float bearing = results[1];
		// float azimuthRotate = -azimuth*360/(2*3.14159f);
		// arrow.setDirection(bearing+azimuthRotate);
	}

	Location userLocation = getLocation(50.066389, -5.71472);

	private void calculateDirection2() {
		float azimuth = sensorEventListener.getAzimuth();
		azimuth = azimuth * 360 / (2 * (float) Math.PI);
		// userLocation = locationListener.getLocation();

		if (userLocation == null) {
			userLocation = getLocation(50.066389, -5.71472);
		}
		GeomagneticField userGeoField = getGeoField(userLocation);

		Location patientLocation = getLocation(58.64389, -3.07);
		// GeomagneticField patientGeoLocation = getGeoField(patientLocation);

		float heading = Double.valueOf(azimuth).floatValue();
		// float heading = userLocation.get
		float bearingDistanceInAngleOfTrueNorth = userLocation
				.bearingTo(patientLocation);
		// to adjust the declination
		heading += userGeoField.getDeclination();

		// heading = bearingDistanceInAngleOfTrueNorth -
		// (bearingDistanceInAngleOfTrueNorth + heading);
		// float finalAngle = Math.round(-heading/360.0f + 180.0f);
		// arrow.setDirection(finalAngle);

		float direction = heading - bearingDistanceInAngleOfTrueNorth;
		 arrow.setDirection(-direction);
		//locationView.setDirection(-direction, userLocation, patientLocation);

		allValues.setText("H" + azimuth + " | UserLocation:"
				+ userLocation.getLatitude() + ","
				+ userLocation.getLongitude() + " | beaingDistance"
				+ bearingDistanceInAngleOfTrueNorth + " Final angle");

		float distanceBetweenPoints = userLocation.distanceTo(patientLocation);
		distance.setText("Distance : " + Float.toString(distanceBetweenPoints)
				+ "m");
	}

	@Override
	public void onResume() {
		super.onResume();
		sensorManager.registerListener(sensorEventListener,
				sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER),
				SensorManager.SENSOR_DELAY_NORMAL);
		sensorManager.registerListener(sensorEventListener,
				sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD),
				SensorManager.SENSOR_DELAY_NORMAL);
		locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0,
				0, locationListener);
	}

	@Override
	public void onPause() {
		super.onPause();
		sensorManager.unregisterListener(sensorEventListener);
		locationManager.removeUpdates(locationListener);
	}

	private LinearLayout getActionLayout() {
		LinearLayout actionLayout = new LinearLayout(this);
		actionLayout.setOrientation(0);
		actionLayout.setGravity(0x77);
		Button found = getButton("Found");
		actionLayout.addView(found);
		actionLayout.addView(getButton("Not Found"));
		actionLayout.addView(getButton("Call"));
		Button simulateButton = getButton("Simulate");
		actionLayout.addView(simulateButton);

		found.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				Intent intent = new Intent(LocationActivity.this,
						SelectFormActivity.class);
				startActivity(intent);
			}
		});
		simulateButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View view) {
				calculateDirection2();
			}
		});
		return actionLayout;
	}

	private Location getLocation(double latitude1, double longitude1) {
		Location loc = new Location("");
		loc.setLatitude(latitude1);
		loc.setLongitude(longitude1);
		return loc;
	}

	private Button getButton(String text) {
		Button button1 = new Button(this);
		button1.setText(text);
		button1.setTextColor(ColorStateList.valueOf(Color.WHITE));
		return button1;
	}

	public void updateCompass(float[] orientation) {
		calculateDirection2();
	}

	private GeomagneticField getGeoField(Location loc) {
		return new GeomagneticField(floatVal(loc.getLatitude()),
				floatVal(loc.getLongitude()), floatVal(loc.getAltitude()),
				loc.getTime());
	}

	private float floatVal(double d) {
		return Double.valueOf(d).floatValue();
	}
}