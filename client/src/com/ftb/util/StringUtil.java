package com.ftb.util;

public class StringUtil {

    public static boolean isNullOrEmpty(String text){
        return text == null &&  "".equals(text.trim());
    }

    public static boolean isNotNullOrEmpty(String text){
        return text !=null && !"".equals(text.trim());
    }
}
