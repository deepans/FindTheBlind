package com.ftb.model;

import android.content.Context;
import com.activeandroid.ActiveRecordBase;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.google.gson.JsonParser;

@Table(name = "PatientDetail")
public class PatientDetail extends ActiveRecordBase<PatientDetail> {

    public PatientDetail(Context context) {
        super(context);
    }

    @Column(name = "pdid")
    public String pk;

    @Column(name = "age")
    public String age;

    @Column(name = "sex")
    public String sex;

    @Column(name = "ethnic_group")
    public String ethnic_group;

    @Column(name = "visual_loss_age")
    public String visual_loss_age;

    @Column(name="patient")
    public Patient p;

    @Column(name="version")
    public String version;

    public void saveInfo(Context context,String patientListJson){

        JsonParser jsonParser = new JsonParser();
    }
}