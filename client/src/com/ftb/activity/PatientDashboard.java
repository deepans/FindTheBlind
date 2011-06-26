package com.ftb.activity;

import android.app.Activity;
import android.app.TabActivity;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TabHost;
import com.ftb.R;


public class PatientDashboard extends TabActivity{
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.dashboard);

        Bundle extras = getIntent().getExtras();
        setTitle(extras.getString("name"));

        TabHost tabHost = getTabHost();
        tabHost.addTab(tabHost.newTabSpec("Locate").setIndicator("Locate").setContent(new Intent(this, LocatePatient.class)));
        Intent intent = new Intent(this, ViewPatient.class);
        intent.putExtra("id", extras.getString("id"));
        intent.putExtra("name", extras.getString("name"));
        tabHost.addTab(tabHost.newTabSpec("Details").setIndicator("Details").setContent(intent));
        tabHost.setCurrentTab(0);
    }
}