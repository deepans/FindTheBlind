package com.ftb.generator;

import android.content.Context;
import android.graphics.Color;
import android.util.TypedValue;
import android.view.inputmethod.EditorInfo;
import android.widget.EditText;
import android.widget.TextView;

public class FormLabel extends FormWidget
{
	protected TextView _label;

	public FormLabel(Context context, String property)
	{
		super( context, property );
		
		_label = new TextView( context );
		_label.setText( getDisplayText() );
		_label.setLayoutParams(FormActivity.defaultLayoutParams);
        _label.setTextColor(Color.BLACK);
        _label.setTextSize(TypedValue.COMPLEX_UNIT_PX,18);

		_layout.addView( _label );
	}
	
	@Override
	public boolean isValueWidget(){
        return false;
    }

}
