package com.ftb.model;

import android.content.Context;
import com.activeandroid.ActiveRecordBase;
import com.activeandroid.annotation.Column;
import com.activeandroid.annotation.Table;

import java.util.ArrayList;

@Table(name = "CredentialInfo")
public class CredentialInfo extends ActiveRecordBase<CredentialInfo> {

    public CredentialInfo(Context context) {
        super(context);
    }

    @Column(name = "username")
    public String username;

    @Column(name = "passwd")
    public String passwd;


    public static void saveCredentialInfo(Context context, LoginInfoModel loginInfoModel) {

        CredentialInfo credentialInfo = new CredentialInfo(context);
        credentialInfo.username= loginInfoModel.userName;
        credentialInfo.passwd = loginInfoModel.passwd;
        credentialInfo.save();
    }
}