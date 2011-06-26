package com.ftb.util;

import android.content.Context;
import com.activeandroid.ActiveRecordBase;

import java.util.ArrayList;

public class ActiveRecordUtil {

    private static ActiveRecordUtil activeRecordUtil = new ActiveRecordUtil();
    private static Context context;

    private ActiveRecordUtil() {
    }

    public static ActiveRecordUtil instance(Context context) {
        ActiveRecordUtil.context = context;
        return activeRecordUtil;
    }

    public <T extends ActiveRecordBase<T>> void deleteAll(Class<T> clazz) {
        ArrayList<T> list = T.query(context, clazz, null, null, null);
        for (T info : list) {
            info.delete();
        }
    }
}