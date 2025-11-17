import { useEffect, useState } from 'react';
import { supabase, Client } from '../lib/supabase';
import {
  Users,
  Clock,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Calendar
} from 'lucide-react';

interface DashboardStats {
  total: number;
  pending: number;
  inReview: number;
  approved: number;
  highPriority: number;
  recentFilings: number;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats>({
    total: 0,
    pending: 0,
    inReview: 0,
    approved: 0,
    highPriority: 0,
    recentFilings: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const { data: clients } = await supabase
        .from('clients')
        .select('*');

      if (clients) {
        const thirtyDaysAgo = new Date();
        thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

        setStats({
          total: clients.length,
          pending: clients.filter((c: Client) => c.case_status === 'pending').length,
          inReview: clients.filter((c: Client) => c.case_status === 'in_review').length,
          approved: clients.filter((c: Client) => c.case_status === 'approved').length,
          highPriority: clients.filter((c: Client) => c.priority === 'high' || c.priority === 'urgent').length,
          recentFilings: clients.filter((c: Client) =>
            c.filing_date && new Date(c.filing_date) >= thirtyDaysAgo
          ).length,
        });
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const statCards = [
    { label: 'Total Clients', value: stats.total, icon: Users, color: 'bg-blue-500' },
    { label: 'Pending Cases', value: stats.pending, icon: Clock, color: 'bg-amber-500' },
    { label: 'In Review', value: stats.inReview, icon: TrendingUp, color: 'bg-indigo-500' },
    { label: 'Approved', value: stats.approved, icon: CheckCircle, color: 'bg-green-500' },
    { label: 'High Priority', value: stats.highPriority, icon: AlertCircle, color: 'bg-red-500' },
    { label: 'Recent Filings (30d)', value: stats.recentFilings, icon: Calendar, color: 'bg-slate-500' },
  ];

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse">
            <div className="h-4 bg-slate-200 rounded w-1/2 mb-4"></div>
            <div className="h-8 bg-slate-200 rounded w-1/3"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {statCards.map((stat, index) => (
        <div key={index} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-slate-600 mb-1">{stat.label}</p>
              <p className="text-3xl font-bold text-slate-900">{stat.value}</p>
            </div>
            <div className={`${stat.color} p-3 rounded-lg`}>
              <stat.icon className="w-6 h-6 text-white" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
