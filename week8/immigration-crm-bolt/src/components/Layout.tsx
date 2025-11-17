import { ReactNode } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Scale, LayoutDashboard, Users, LogOut } from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  currentView: 'dashboard' | 'clients';
  onViewChange: (view: 'dashboard' | 'clients') => void;
}

export default function Layout({ children, currentView, onViewChange }: LayoutProps) {
  const { signOut } = useAuth();

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <nav className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-8">
              <div className="flex items-center gap-3">
                <Scale className="w-8 h-8 text-slate-700" />
                <span className="text-xl font-bold text-slate-900">Immigration CRM</span>
              </div>

              <div className="flex gap-1">
                <button
                  onClick={() => onViewChange('dashboard')}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                    currentView === 'dashboard'
                      ? 'bg-slate-100 text-slate-900 font-medium'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <LayoutDashboard className="w-5 h-5" />
                  Dashboard
                </button>

                <button
                  onClick={() => onViewChange('clients')}
                  className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-colors ${
                    currentView === 'clients'
                      ? 'bg-slate-100 text-slate-900 font-medium'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                  }`}
                >
                  <Users className="w-5 h-5" />
                  Clients
                </button>
              </div>
            </div>

            <button
              onClick={handleSignOut}
              className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors"
            >
              <LogOut className="w-5 h-5" />
              Sign Out
            </button>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">{children}</main>
    </div>
  );
}
