package com.ftb.activity;

import android.app.Activity;
import android.app.ListActivity;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import com.ftb.R;


public class SelectFormActivity extends ListActivity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        fillData();

    }

    private void fillData() {
        String[] forms = getResources().getStringArray(R.array.forms_array);
        setListAdapter(new ArrayAdapter<String>(this, R.layout.form_item, forms));
    }
}