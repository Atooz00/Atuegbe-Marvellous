import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View } from 'react-native';

export default function App() {
  return (
    <View style={styles.container}>
      <View style={styles.card}>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>GIT PROJECT</Text>
        </View>
        
        <Text style={styles.title}>React Native Mobile</Text>
        
        <View style={styles.divider} />
        
        <Text style={styles.name}>Atuegbe Marvellous A.</Text>
        <Text style={styles.matric}>   RUN/CMP/22/12865
                </Text>
        
        <View style={styles.statusBox}>
          <Text style={styles.statusText}>● System Online</Text>
        </View>
      </View>
      
      <StatusBar style="light" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a2a6c', // Deep professional blue
    alignItems: 'center',
    justifyContent: 'center',
  },
  card: {
    backgroundColor: '#ffffff',
    padding: 30,
    borderRadius: 20,
    width: '90%', // Increased width to 90% to give more room
    alignItems: 'center',
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.3,
  },
  badge: {
    backgroundColor: '#f39c12',
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 10,
    marginBottom: 15,
  },
  badgeText: {
    color: '#fff',
    fontSize: 10,
    fontWeight: 'bold',
  },
  title: {
    fontSize: 24,
    fontWeight: '900',
    color: '#1a2a6c',
    marginBottom: 10,
  },
  divider: {
    height: 2,
    backgroundColor: '#eee',
    width: '100%',
    marginVertical: 15,
  },
  name: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
  },
  matric: {
    fontSize: 16, // Slightly smaller font to ensure it fits
    color: '#666',
    marginTop: 5,
    textAlign: 'center', // Ensures it stays centered if it wraps
    width: '100%', // Takes up the full width of the card
  },
  statusBox: {
    marginTop: 25,
    backgroundColor: '#e8f5e9',
    paddingHorizontal: 15,
    paddingVertical: 5,
    borderRadius: 20,
  },
  statusText: {
    color: '#2e7d32',
    fontSize: 12,
    fontWeight: 'bold',
  }
});