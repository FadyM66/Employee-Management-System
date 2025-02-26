import { useFormik } from 'formik';
import { loginSchema } from '../schemas/schema.js';
import { handleLoginSubmit } from './LoginUtils.js';
import { useState } from 'react';

export const useLoginForm = () => {

  const [ submissionResult, setSubmissionResult ] = useState();

  const formik = useFormik({
    initialValues: {
      email: "",
      password: "",
    },
    validationSchema: loginSchema,
    onSubmit: async (values, formikHelpers) => {
      await handleLoginSubmit(values, formikHelpers, setSubmissionResult);
    }
  });

  return {
    values: formik.values,
    errors: formik.errors,
    touched: formik.touched,
    isSubmitting: formik.isSubmitting,
    handleChange: formik.handleChange,
    handleBlur: formik.handleBlur,
    handleSubmit: formik.handleSubmit,
    submissionResult 
  };
};