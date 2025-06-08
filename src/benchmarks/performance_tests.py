import time
import matplotlib.pyplot as plt
import numpy as np
from ..crypto.hybrid_encryption import HybridECCAES

class PerformanceBenchmark:
    def __init__(self):
        """Initialize benchmark suite."""
        self.hybrid_system = HybridECCAES()
        self.results = {}
    
    def benchmark_encryption_sizes(self, sizes=[1024, 10240, 102400, 1024000]):
        """
        NOVELTY: Benchmark hybrid ECC-AES vs traditional RSA-AES.
        Compare performance across different data sizes.
        """
        print("🔬 Benchmarking Hybrid ECC-AES Performance...")
        
        ecc_times = []
        
        for size in sizes:
            # Generate test data
            test_data = "A" * size
            
            # Benchmark ECC-AES
            start_time = time.time()
            encrypted_package = self.hybrid_system.encrypt_workload(
                test_data, 
                cloud_region="us-east-1", 
                workload_type="benchmark"
            )
            decrypted_result = self.hybrid_system.decrypt_workload(encrypted_package)
            ecc_time = time.time() - start_time
            
            ecc_times.append(ecc_time * 1000)  # Convert to milliseconds
            
            print(f"Data size: {size:,} bytes, ECC-AES time: {ecc_time*1000:.2f}ms")
        
        self.results['sizes'] = sizes
        self.results['ecc_times'] = ecc_times
        
        return self.results
    
    def benchmark_curve_comparison(self):
        """
        NOVELTY: Compare different ECC curves for cloud workloads.
        """
        curves = ["secp256r1", "secp384r1", "secp521r1"]
        test_data = "Cloud workload test data " * 100
        
        curve_results = {}
        
        for curve in curves:
            hybrid_system = HybridECCAES(ecc_curve=curve)
            
            start_time = time.time()
            encrypted_package = hybrid_system.encrypt_workload(test_data)
            decrypted_result = hybrid_system.decrypt_workload(encrypted_package)
            total_time = time.time() - start_time
            
            curve_results[curve] = total_time * 1000
            print(f"Curve {curve}: {total_time*1000:.2f}ms")
        
        return curve_results
    
    def plot_performance_results(self):
        """Visualize benchmark results."""
        if 'sizes' not in self.results:
            print("No benchmark data available. Run benchmark_encryption_sizes() first.")
            return
        
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Encryption time vs data size
        plt.subplot(2, 2, 1)
        plt.plot(self.results['sizes'], self.results['ecc_times'], 'bo-', label='Hybrid ECC-AES')
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Encryption Time (ms)')
        plt.title('Encryption Performance vs Data Size')
        plt.legend()
        plt.grid(True)
        
        # Plot 2: Throughput
        plt.subplot(2, 2, 2)
        throughput = [size / (time/1000) for size, time in zip(self.results['sizes'], self.results['ecc_times'])]
        plt.plot(self.results['sizes'], throughput, 'ro-')
        plt.xlabel('Data Size (bytes)')
        plt.ylabel('Throughput (bytes/second)')
        plt.title('Encryption Throughput')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('hybrid_ecc_aes_performance.png', dpi=300, bbox_inches='tight')
        plt.show()
