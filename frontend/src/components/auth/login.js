import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { Password } from 'primereact/password';
import { NavLink, useNavigate } from 'react-router-dom';
import { APIgatewayService } from '../../services';
import { useReducer } from 'react';
import { Toast } from 'primereact/toast';
import { useRef } from 'react';

export const Login = () => {
  const navigate = useNavigate();
  const toast = useRef(null);
  let service = new APIgatewayService();
  const initialForm = {
    username: '',
    password: ''
  };
  const [form, updateForm] = useReducer(
    (state, updates) => ({ ...state, ...updates }),
    initialForm
  );

  const fetchData = async () => {
    return await service.login(form);
  };
  const handleResponse = (response) => {
    if (!response.ok) {
      toast.current.show({
        severity: 'error',
        summary: 'Authentication',
        detail: 'Wrong credentials',
        life: 3000
      });
    } else {
      navigate('/dashboard');
    }
  };
  const onSubmit = async () => {
    let response = await fetchData();
    handleResponse(response);
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
          <h5>Password</h5>
          <Password
            value={form.password}
            onChange={(e) => updateForm({ password: e.target.value })}
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
        <NavLink to="/register"> Need an account? </NavLink>
      </form>
    </div>
  );
};
