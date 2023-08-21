import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Login } from './components/auth/login';
import { Register } from './components/auth/register';
import { PageNotFound } from './components/errors/404notfound';
import { CommonDashboard } from './components/dashboard/commonDashboard';
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<CommonDashboard />} />
        <Route path="*" element={<PageNotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
