package com.ftb.util;

import android.content.Context;
import com.ftb.model.Address;
import com.ftb.model.FamilyHistory;
import com.ftb.model.Patient;
import com.ftb.model.PatientDetail;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.InstanceCreator;
import com.google.gson.JsonParser;

import java.lang.reflect.Type;

public class GsonUtil {

    private static Context context;
    private Gson gson;

    private GsonUtil() {
    }

    public static GsonUtil instance(Context context) {
        GsonUtil.context = context;
        return new GsonUtil();
    }

    public Gson getGson() {

        if(gson == null){
            GsonBuilder gsonBuilder = new GsonBuilder();

            gsonBuilder.registerTypeAdapter(Patient.class, getInstanceCreator(context, Patient.class));
            gsonBuilder.registerTypeAdapter(PatientDetail.class, getInstanceCreator(context, PatientDetail.class));
            gsonBuilder.registerTypeAdapter(FamilyHistory.class, getInstanceCreator(context, FamilyHistory.class));
            gsonBuilder.registerTypeAdapter(Address.class, getInstanceCreator(context, Address.class));

            return gsonBuilder.create();
        }else{
            return gson;
        }
    }

    public <T> InstanceCreator<T> getInstanceCreator(final Context context, final Class<T> clazz) {
        return new InstanceCreator<T>() {
            public T createInstance(Type type) {
                try {
                    return (T) clazz.getConstructor(Context.class).newInstance(context);
                } catch (Exception e) {
                   return null;
                }
            }
        };
    }

    public <T> T[] getArrayData(String jsonData, Class<T[]> clazz) {
        return getGson().fromJson(jsonData, clazz);
    }

    public <T> T getData(final String jsonData, JsonParser jsonParser, Class<T> clazz) {
        return getGson().fromJson(jsonData, clazz);
    }
}