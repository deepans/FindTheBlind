package com.ftb.activity;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import com.ftb.R;
import com.ftb.generator.FormActivity;

import java.util.HashMap;
import java.util.Map;


public class PatientDetailsActivity extends FormActivity {

    public static final int OPTION_SAVE = 0;
	public static final int OPTION_POPULATE = 1;
	public static final int OPTION_CANCEL = 2;
    public static final Map<String,String> formMap = new HashMap<String, String>();

    static{
        formMap.put("Personal Details", "personal_details");
        formMap.put("Visual Assessment", "visual_assessment");
        formMap.put("General Assessment", "general_assessment");
        formMap.put("Previous Eye Surgery", "previous_eye_surgery");
        formMap.put("Eye Examination - site of abnormality", "eye_examination_abnormality");
        formMap.put("Refraction/low vision aid assessment", "refraction");
        formMap.put("Eye Examination - aetiology", "eye_examination_aetiology");
        formMap.put("Action Needed", "action_needed");
        formMap.put("Prognosis for vision", "prognosis");
        formMap.put("Education", "education");
        formMap.put("Full Diagnosis", "full_diagnosis");
        formMap.put("Examiner", "examiner");
    }

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
         generateForm(FormActivity.parseFileToString(this, "previous_eye_surgery.json"));
    }

        @Override
	public boolean onCreateOptionsMenu( Menu menu )
	{
		menu.add( 0, OPTION_SAVE, 0, "Save" );
		menu.add( 0, OPTION_POPULATE, 0, "Populate" );
		menu.add( 0, OPTION_CANCEL, 0, "Cancel" );
		return true;
	}

	@Override
	public boolean onMenuItemSelected( int id, MenuItem item )
	{

		switch( item.getItemId() )
		{
			case OPTION_SAVE:
				save();
				break;

			case OPTION_POPULATE:
				populate( FormActivity.parseFileToString( this, "data.json" ) );
				break;

			case OPTION_CANCEL:

				break;
		}

		return super.onMenuItemSelected( id, item );
	}
}