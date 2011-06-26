package com.ftb.model;

import android.content.Context;
import com.activeandroid.ActiveRecordBase;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.google.gson.JsonParser;

@Table(name = "Patient")
public class Patient extends ActiveRecordBase<Patient> {

    public Patient(Context context) {
        super(context);
    }

    @Column(name = "pid")
    public String pk;

    @Column(name = "name")
    public String name;

    @Column(name="pversion")
    public String version;

    public PatientDetail patientdetails;
    public FamilyHistory familyhistory;
    public Address address;

    public void saveInfo(Context context,String patientListJson){

        JsonParser jsonParser = new JsonParser();
    }

    @Override
    public String toString() {
        return name;
    }

    public static Patient get(Context context, String id) {
        Patient patient = Patient.querySingle(context, Patient.class, null, "pid=" + id);
        patient.patientdetails = queryChild(context, id, PatientDetail.class);
        patient.familyhistory = queryChild(context, id, FamilyHistory.class);
        patient.address= queryChild(context, id, Address.class);

        return patient;
    }

    private static <T extends ActiveRecordBase<T>> T queryChild(Context context, String id, Class<T> clazz) {
        return T.querySingle(context, clazz, null, "patient=" + id);
    }
}