package com.ftb.activity;

import android.app.Activity;
import android.content.Intent;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.hardware.Sensor;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import com.ftb.R;


public class LocationActivity extends Activity {

    private SensorManager sensorManager;
    private SensorLogic sensorEventListener = new SensorLogic();
    private Arrow arrow;
    private LocationManager locationManager;
    private LocationLogic locationListener = new LocationLogic();

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.location);
        LinearLayout layout = (LinearLayout)findViewById(R.id.location);

        arrow = new Arrow(this);
        LinearLayout actionLayout = getActionLayout();

        layout.addView(arrow);
        layout.addView(actionLayout);

        sensorManager = (SensorManager) getSystemService(SENSOR_SERVICE);
        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

        float azimuth = sensorEventListener.getAzimuth();
        Location userLocation = locationListener.getLocation();

        if(userLocation == null){
            userLocation = getLocation(50.066389, -5.71472);
        }

        Location patientLocation = getLocation(58.64389, -3.07);

        float[] results = new float[3];
        Location.distanceBetween(userLocation.getLatitude(), userLocation.getLongitude(),patientLocation.getLatitude(),patientLocation.getLongitude(), results);

        float bearing = results[1];
        float azimuthRotate = -azimuth*360/(2*3.14159f);
        arrow.setDirection(bearing+azimuthRotate);
    }

    @Override
      public void onResume() {
        super.onResume();
        sensorManager.registerListener(sensorEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), SensorManager.SENSOR_DELAY_NORMAL);
        sensorManager.registerListener(sensorEventListener, sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD), SensorManager.SENSOR_DELAY_NORMAL);
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER,0,0, locationListener);
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

        found.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(LocationActivity.this, SelectFormActivity.class);
                startActivity(intent);
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
}