package com.ftb.activity;

import android.app.Activity;
import android.app.TabActivity;
import android.content.Intent;
import android.content.res.Resources;
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
        Resources res = getResources();
        tabHost.addTab(tabHost.newTabSpec("Locate").setIndicator("Locate", res.getDrawable(R.drawable.ic_menu_preferences)).setContent(new Intent(this, LocatePatient.class)));

        Intent intent = new Intent(this, ViewPatient.class);
        intent.putExtra("id", extras.getString("id"));
        intent.putExtra("name", extras.getString("name"));
        tabHost.addTab(tabHost.newTabSpec("Details").setIndicator("Details", res.getDrawable(R.drawable.recent_checkins_tab_selected)).setContent(intent));
        tabHost.setCurrentTab(0);
    }
}