package com.ftb.util;

import android.content.Context;
import android.widget.DatePicker;
import android.widget.LinearLayout;
import android.widget.TimePicker;

public class DateAndTimePicker extends android.widget.FrameLayout{
    private Context context;
    private LinearLayout dateAndTimeLayout;

    public DateAndTimePicker(Context context) {
        super(context);
        this.context = context;
        dateAndTimeLayout = createDateAndTimePicker();
        addView(dateAndTimeLayout);
    }

    LinearLayout createDateAndTimePicker() {
        LinearLayout linearLayout = new LinearLayout(context);
        linearLayout.setOrientation(LinearLayout.VERTICAL);
        linearLayout.addView(new DatePicker(context));
        linearLayout.addView(new TimePicker(context));
        return linearLayout;
    }

    public String getValue(){
        DatePicker datePicker = (DatePicker)dateAndTimeLayout.getChildAt(0);
        String date = String.valueOf(datePicker.getDayOfMonth())+"-"+String.valueOf(datePicker.getMonth()+1)+"-"+String.valueOf(datePicker.getYear());
        TimePicker timePicker = (TimePicker)dateAndTimeLayout.getChildAt(1);
        String time = timePicker.getCurrentHour().toString()+":"+timePicker.getCurrentMinute().toString();
        return (date + " " +time);
    }
}