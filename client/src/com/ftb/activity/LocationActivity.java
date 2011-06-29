package com.ftb.activity;

import android.app.Activity;
import android.content.Intent;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.location.Location;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import com.ftb.R;


public class LocationActivity extends Activity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.location);
        LinearLayout layout = (LinearLayout)findViewById(R.id.location);
        final Arrow arrow = new Arrow(this);
        layout.addView(arrow);

        LinearLayout actionLayout = new LinearLayout(this);
        actionLayout.setOrientation(0);
        actionLayout.setGravity(0x77);
        Button found = getButton("Found");
        actionLayout.addView(found);
        actionLayout.addView(getButton("Not Found"));
        actionLayout.addView(getButton("Call"));
        layout.addView(actionLayout);

        found.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(LocationActivity.this, SelectFormActivity.class);
                startActivity(intent);
            }
        });

        Location loc = getLocation(50.066389, -5.71472);
        Location loc1 = getLocation(58.64389, -3.07);

        float[] results = new float[3];
        Location.distanceBetween(loc.getLatitude(),loc.getLongitude(),loc1.getLatitude(),loc1.getLongitude(), results);

        arrow.setDirection(results[1]);
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