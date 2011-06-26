package com.ftb.model;

import android.content.Context;
import com.activeandroid.ActiveRecordBase;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;
import com.google.gson.JsonParser;

@Table(name = "Address")
public class Address extends ActiveRecordBase<Address> {

    public Address(Context context) {
        super(context);
    }

    @Column(name = "aid")
    public String pk;

    @Column(name = "town")
    public String town;

    @Column(name = "city")
    public String city;

    @Column(name="patient")
    public Patient p;

    @Column(name="version")
    public String version;

    public void saveInfo(Context context,String patientListJson){

        JsonParser jsonParser = new JsonParser();
    }
}