package com.ftb.model;

import com.google.gson.Gson;


public class LoginInfoModel {

    public String passwd;
    public String userName;

    public String toJson() {
        return new Gson().toJson(this);
    }
}
