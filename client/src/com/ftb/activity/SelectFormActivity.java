package com.ftb.activity;

import android.app.Activity;
import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import com.ftb.R;


public class SelectFormActivity extends ListActivity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        fillData();
        getListView().setOnItemClickListener(listener());
    }

   private AdapterView.OnItemClickListener listener() {
        return new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {
                String formName = (String) getListAdapter().getItem(position);
                Intent intent = new Intent(SelectFormActivity.this, PatientDetailsActivity.class);
                intent.putExtra("form_name", formName);
                startActivity(intent);
            }
        };
    }

    private void fillData() {
        String[] forms = getResources().getStringArray(R.array.forms_array);
        setListAdapter(new ArrayAdapter<String>(this, R.layout.form_item, forms));
    }
}