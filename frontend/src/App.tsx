import './App.css'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from '@/components/providers/AuthProvider'
import { Toaster } from '@/components/ui/sonner'
// import SignUp from './pages/SignUp'
// import SignIn from './pages/SignIn'
import Navbar from './components/Navbar'
import HomePage from './pages/home-page'

const queryClient = new QueryClient()

function App() {
  return (
    <div className='App'>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Navbar />
          <Router>
            <Routes>
              <Route path='/' element={<HomePage />} />
              {/* <Route path='/signup' element={<SignUp />} />
              <Route path='/login' element={<SignIn />} /> */}
            </Routes>
          </Router>
          <Toaster />
        </AuthProvider>
      </QueryClientProvider>
    </div>
  )
}

export default App
