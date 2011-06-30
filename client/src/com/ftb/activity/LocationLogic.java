package com.ftb.activity;

import android.location.Location;
import android.location.LocationListener;
import android.os.Bundle;

public class LocationLogic implements LocationListener{

    private Location location;

    @Override
    public void onLocationChanged(Location location) {
         this.location = location;
    }

    @Override
    public void onStatusChanged(String s, int i, Bundle bundle) {
    }

    @Override
    public void onProviderEnabled(String s) {
    }

    @Override
    public void onProviderDisabled(String s) {
    }

    public Location getLocation() {
        return location;
    }
}
