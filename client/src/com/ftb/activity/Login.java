package com.ftb.activity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import com.ftb.R;
import com.ftb.model.LoginInfoModel;
import com.ftb.model.Patient;
import com.ftb.util.ActiveRecordUtil;
import com.ftb.util.GsonUtil;

public class Login extends Activity {

    public void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.login);
        findViewById(R.id.login).setOnClickListener(createButtonClickListener());

    }


    private String getTextData(int editTextElementId) {
        return ((EditText) findViewById(editTextElementId)).getText().toString();
    }

    public View.OnClickListener createButtonClickListener() {

        return new View.OnClickListener() {

            public void onClick(View v) {
                setupData();
                LoginInfoModel loginInfoModel = getModel();
                Intent intent = new Intent(Login.this, PatientList.class);
                startActivity(intent);
            }
        };
    }

    private void setupData() {
        ActiveRecordUtil.instance(this).deleteAll(Patient.class);
        String json = "[\n" +
                "    {\n" +
                "        \"patientdetails\": {\n" +
                "            \"patient\": 1,\n" +
                "            \"visual_loss_age\": 99,\n" +
                "            \"age\": 29,\n" +
                "            \"sex\": \"M\",\n" +
                "            \"ethnic_group\": \"Hindu\",\n" +
                "            \"version\": 1,\n" +
                "            \"pk\": 1,\n" +
                "            \"model\": \"ftb.patientdetails\"\n" +
                "        },\n" +
                "        \"_locked_by\": null,\n" +
                "        \"_hard_lock\": false,\n" +
                "        \"version\": 1,\n" +
                "        \"familyhistory\": {\n" +
                "            \"has_family_history\": true,\n" +
                "            \"version\": 1,\n" +
                "            \"patient\": 1,\n" +
                "            \"affected_relation\": \"Uncle\",\n" +
                "            \"pk\": 1,\n" +
                "            \"model\": \"ftb.familyhistory\",\n" +
                "            \"consanguinity\": false\n" +
                "        },\n" +
                "        \"address\": {\n" +
                "            \"town\": \"Neyveli\",\n" +
                "            \"pk\": 1,\n" +
                "            \"model\": \"ftb.address\",\n" +
                "            \"version\": 1,\n" +
                "            \"patient\": 1\n" +
                "        },\n" +
                "        \"_locked_at\": null,\n" +
                "        \"pk\": 1,\n" +
                "        \"model\": \"ftb.patient\",\n" +
                "        \"name\": \"DeepanS\"\n" +
                "    },\n" +
                "    {\n" +
                "        \"patientdetails\": {\n" +
                "            \"patient\": 2,\n" +
                "            \"visual_loss_age\": 99,\n" +
                "            \"age\": 29,\n" +
                "            \"sex\": \"M\",\n" +
                "            \"ethnic_group\": \"Hindu\",\n" +
                "            \"version\": 1,\n" +
                "            \"pk\": 2,\n" +
                "            \"model\": \"ftb.patientdetails\"\n" +
                "        },\n" +
                "        \"_locked_by\": null,\n" +
                "        \"_hard_lock\": false,\n" +
                "        \"version\": 1,\n" +
                "        \"familyhistory\": {\n" +
                "            \"has_family_history\": true,\n" +
                "            \"version\": 1,\n" +
                "            \"patient\": 2,\n" +
                "            \"affected_relation\": \"Uncle\",\n" +
                "            \"pk\": 2,\n" +
                "            \"model\": \"ftb.familyhistory\",\n" +
                "            \"consanguinity\": false\n" +
                "        },\n" +
                "        \"address\": {\n" +
                "            \"town\": \"Neyveli\",\n" +
                "            \"pk\": 2,\n" +
                "            \"model\": \"ftb.address\",\n" +
                "            \"version\": 1,\n" +
                "            \"patient\": 2\n" +
                "        },\n" +
                "        \"_locked_at\": null,\n" +
                "        \"pk\": 2,\n" +
                "        \"model\": \"ftb.patient\",\n" +
                "        \"name\": \"Aruns\"\n" +
                "    }\n" +
                "]";

        Patient[] patients = GsonUtil.instance(this).getArrayData(json, Patient[].class);

        for(Patient patient: patients){

            patient.address.p = patient;
            patient.familyhistory.p = patient;
            patient.patientdetails.p = patient;
            patient.save();
            patient.patientdetails.save();
            patient.familyhistory.save();
            patient.address.save();
        }

    }

    public LoginInfoModel getModel() {

        LoginInfoModel loginInfoModel = new LoginInfoModel();
        loginInfoModel.passwd =   getTextData(R.id.pass);
        loginInfoModel.userName = getTextData(R.id.uName);

        return loginInfoModel;
    }
}