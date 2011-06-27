package com.ftb.activity;

import android.content.Context;
import android.graphics.Color;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.TextView;
import com.ftb.R;
import com.ftb.model.Patient;

import java.util.List;

public class PatientListAdapter extends BaseAdapter {

    private List<Patient> patients;
    private LayoutInflater inflator;

    public PatientListAdapter(Context context, List<Patient> patients) {
        this.patients = patients;
        this.inflator = LayoutInflater.from(context);
    }

    @Override
    public int getCount() {
        return patients.size();
    }

    @Override
    public Patient getItem(int position) {
        return patients.get(position);
    }

    @Override
    public long getItemId(int position) {
        return Long.parseLong(patients.get(position).pk);
    }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Patient patient = getItem(position);

        if(convertView == null){
            convertView = inflator.inflate(R.layout.list_item, null);
        }

        ((TextView)convertView.findViewById(R.id.primary)).setText(patient.name);
        String text = patient.getAge() + " " + patient.getTown();
        ((TextView)convertView.findViewById(R.id.secondary)).setText(text);

        return convertView;
    }
}
