package com.ftb.model;

import android.content.Context;
import com.activeandroid.ActiveRecordBase;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.google.gson.JsonParser;

@Table(name = "FamilyHistory")
public class FamilyHistory extends ActiveRecordBase<FamilyHistory> {

    public FamilyHistory(Context context) {
        super(context);
    }

    @Column(name = "fhid")
    public String pk;

    @Column(name = "isPresent")
    public Boolean has_family_history;

    @Column(name = "affectedRelation")
    public String affected_relation;

    @Column(name="patient")
    public Patient p;

    @Column(name="version")
    public String version;

    public void saveInfo(Context context,String patientListJson){

        JsonParser jsonParser = new JsonParser();
    }
}