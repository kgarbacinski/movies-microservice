import { InputText } from 'primereact/inputtext';
import { Password } from 'primereact/password';
import { Button } from 'primereact/button';
import { NavLink } from 'react-router-dom';
import { useReducer, useRef } from 'react';
import { Toast } from 'primereact/toast';
import { APIgatewayService } from '../../services';
import { useNavigate } from 'react-router-dom';
import { sleep } from '../../utils';

export const Register = () => {
  let service = new APIgatewayService();
  const navigate = useNavigate();
  const toast = useRef(null);
  const initialForm = {
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
    firstName: '',
    lastName: ''
  };
  const [form, updateForm] = useReducer(
    (state, updates) => ({ ...state, ...updates }),
    initialForm
  );

  const fetchData = async () => {
    return await service.register(form);
  };
  const validate = () => {
    let isValid = true;
    if (form.password !== form.confirmPassword) {
      toast.current.show({
        severity: 'error',
        summary: 'Password',
        detail: 'Passwords are not the same',
        life: 3000
      });

      isValid = false;
    }
    if (
      !form.password ||
      !form.username ||
      !form.confirmPassword ||
      !form.email ||
      !form.firstName ||
      !form.lastName
    ) {
      toast.current.show({
        severity: 'error',
        summary: 'Fields',
        detail: 'Fields cannot be empty',
        life: 3000
      });
      isValid = false;
    }
    return isValid;
  };
  const handleResponse = async () => {
    let response = await fetchData();

    if (response.status === 201) {
      toast.current.show({
        severity: 'success',
        summary: 'Account Created!',
        detail: '',
        life: 3000
      });
      await sleep(2000);
      navigate('/login');
    } else {
      const error = await response.json();
      toast.current.show({
        severity: 'error',
        summary: 'Error',
        detail: error.detail.errorMessage,
        life: 3000
      });
    }
  };
  const onSubmit = async () => {
    const isValid = validate();
    if (isValid) {
      await handleResponse();
    }
  };
  return (
    <div>
      <Toast ref={toast} />
      <form>
        <div className="card">
          <h5>Username</h5>
          <InputText
            value={form.username}
            onChange={(e) => updateForm({ username: e.target.value })}
          />
        </div>
        <div className="card">
          <h5>Email</h5>
          <InputText
            value={form.email}
            onChange={(e) => updateForm({ email: e.target.value })}
          />
        </div>
        <div className="card">
          <h5>First Name</h5>
          <InputText
            value={form.firstName}
            onChange={(e) => updateForm({ firstName: e.target.value })}
          />
        </div>
        <div className="card">
          <h5>Last name</h5>
          <InputText
            value={form.lastName}
            onChange={(e) => updateForm({ lastName: e.target.value })}
          />
        </div>
        <div className="card">
          <h5>Password</h5>
          <Password
            value={form.password}
            onChange={(e) => updateForm({ password: e.target.value })}
            feedback={false}
          />
        </div>
        <div className="card">
          <h5>Confirm Password</h5>
          <Password
            value={form.confirmPassword}
            onChange={(e) => updateForm({ confirmPassword: e.target.value })}
            feedback={false}
          />
        </div>

        <div>
          <Button
            label="Submit"
            aria-label="Submit"
            type="button"
            onClick={onSubmit}
          />
        </div>
        <NavLink to="/login"> Login </NavLink>
      </form>
    </div>
  );
};
