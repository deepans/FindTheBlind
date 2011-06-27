package com.ftb.activity;

import android.app.Activity;
import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import com.ftb.R;
import com.ftb.model.Patient;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;


public class PatientList extends ListActivity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        fillData();
        getListView().setOnItemClickListener(listener());
    }

    private void fillData() {
        List<Patient> resultList = getPatientList();
        setListAdapter(new PatientListAdapter(this, resultList));
    }

    private List<Patient> getPatientList() {
        return Patient.query(this, Patient.class, null, null, null);
    }

    private AdapterView.OnItemClickListener listener() {
        return new AdapterView.OnItemClickListener() {
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long l) {
                Patient patient = getItem(position);
                Intent intent = new Intent(getApplicationContext(), PatientDashboard.class);
                intent.putExtra("id", patient.pk);
                intent.putExtra("name", patient.name);
                startActivity(intent);
            }
        };
    }

    private Patient getItem(int position){
        return(Patient) getListAdapter().getItem(position);
    }

}