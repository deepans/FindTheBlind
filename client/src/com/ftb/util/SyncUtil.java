package com.ftb.util;

import android.content.Context;
import android.os.Looper;
import android.widget.Toast;
import com.google.gson.JsonParser;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import java.util.*;


public class SyncUtil {

    private static SyncUtil syncUtil = new SyncUtil();

    private SyncUtil() {
    }

    public static SyncUtil instance() {
        return syncUtil;
    }


    public String doPost(String url, Map<String, String> kvPairs) {
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost(url);

        try {
            if (kvPairs != null && kvPairs.isEmpty() == false) {
                List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>(kvPairs.size());
                String k, v;
                Iterator<String> itKeys = kvPairs.keySet().iterator();
                while (itKeys.hasNext()) {
                    k = itKeys.next();
                    v = kvPairs.get(k);
                    nameValuePairs.add(new BasicNameValuePair(k, v));
                }
                httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));
            }
            HttpResponse response = httpclient.execute(httppost);


                String responseText = EntityUtils.toString(response.getEntity());
        } catch (Exception ignored) {
            return IConstants.SERVER_DOWN_MESSAGE;
        }

        return IConstants.FAILURE;
    }

}