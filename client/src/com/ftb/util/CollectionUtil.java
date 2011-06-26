package com.ftb.util;

import java.util.*;

public class CollectionUtil {

    public static boolean DEBUG = false;

    public static <T> String join(String separator, Collection<T> valuesOriginal) {
        if (valuesOriginal == null) return "";
        ArrayList<T> values = new ArrayList<T>(valuesOriginal);
        removeAllNullEntries(values);
        if (separator == null) {
            separator = "";
        }
        if (values.isEmpty()) {
            return "";
        }
        String joinedString = "";
        for (T value : values) {
            String valueString =  value.toString();
            if (valueString != null && !isEmpty(valueString)) {
                joinedString += valueString + separator;
            }
        }
        return isEmpty(joinedString) ? "" : joinedString.substring(0, joinedString.length() - separator.length());
    }

    private static boolean isEmpty(String valueString) {
        return "".equals(valueString.trim());
    }

    public static <T> String join(String separator, T... values) {
        return join(separator, asList(values));
    }

    public static <T> ArrayList<T> asList(T... values) {
        ArrayList<T> list = new ArrayList<T>();
        for (T value : values) {
            if (value != null)
                list.add(value);
        }
        return list;
    }

    public static <T> ArrayList<T> combineLists(ArrayList... lists) {
        ArrayList<T> list = new ArrayList<T>();
        for (ArrayList<T> value : lists) {
            if (value != null)
                list.addAll(value);
        }
        return list;
    }

    public static void removeAllNullEntries(Collection values) {
        while (values.remove(null)) ;
    }

    public static <T> boolean listsContainSameValuesInSameOrder(List<T> values, List<T> otherValues) {
        if (values.size() != otherValues.size()) return false;

        for (int i = 0; i < values.size(); i++) {
            if (!values.get(i).equals(otherValues.get(i))) return false;
        }
        return true;
    }

    public static <T> boolean any(List<T> values, Predicate<T> predicate) {
        for (T value : values) {
            if (predicate.evaluate(value)) {
                if (DEBUG) System.out.println("success match" + value.getClass().getName());
                return true;
            }
        }
        if (DEBUG) System.out.println("failure match");
        return false;
    }

    public static <T> boolean every(List<T> values, Predicate<T> predicate) {
        for (T value : values) {
            if (!predicate.evaluate(value)) return false;
        }
        return true;
    }

    public static <T> boolean isBlank(List<T> list) {
        return list == null || list.isEmpty();
    }

    public static <T> Set<T> asSet(T... values) {
        HashSet<T> set = new HashSet<T>();
        for (T value : values)
            set.add(value);
        return set;
    }

    public static <T> String suffixAndJoin(String suffix, String delimiter, Collection<T> values) {
        String result = join(suffix + delimiter, values);
        return isEmpty(result) ? result: result + suffix;
    }
}