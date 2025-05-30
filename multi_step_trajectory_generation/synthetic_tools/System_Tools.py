import os
import time
import json
import uuid
import random
import shutil
import subprocess
from urllib.parse import urlparse
from typing import Dict, Any, List, Optional, Union


def execute_command(
    command: str,
    timeout: Optional[int] = 30,
    working_dir: Optional[str] = None,
    env_vars: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Simulates executing a shell command
    
    Args:
        command: The command to execute
        timeout: Maximum execution time in seconds
        working_dir: Working directory for command execution
        env_vars: Additional environment variables
    """
    def sanitize_command(cmd: str) -> bool:
        # Simulate basic command validation
        dangerous_commands = ['rm -rf /', 'mkfs', 'dd', ':(){:|:&};:']
        return not any(dc in cmd for dc in dangerous_commands)
    
    # Validate input
    if not command:
        return {
            "success": False,
            "exit_code": 1,
            "stdout": "",
            "stderr": "Error: Command cannot be empty",
            "error": "Invalid command"
        }
    
    # Basic command safety check
    if not sanitize_command(command):
        return {
            "success": False,
            "exit_code": 126,
            "stdout": "",
            "stderr": "Error: Potentially dangerous command detected",
            "error": "Command rejected for safety reasons"
        }
    
    # Simulate command execution
    current_time = time.time()
    
    # Simulate different command behaviors
    if command.startswith('ls'):
        return {
            "success": True,
            "exit_code": 0,
            "stdout": "file1.txt\nfile2.jpg\ndirectory1/\n",
            "stderr": "",
            "execution_time": 0.02,
            "working_directory": working_dir or "/current/path"
        }
    elif command.startswith('pwd'):
        return {
            "success": True,
            "exit_code": 0,
            "stdout": working_dir or "/current/path",
            "stderr": "",
            "execution_time": 0.01
        }
    elif command.startswith('echo'):
        echo_content = command[5:] if len(command) > 5 else ""
        return {
            "success": True,
            "exit_code": 0,
            "stdout": echo_content + "\n",
            "stderr": "",
            "execution_time": 0.01
        }
    else:
        # Generic command simulation
        return {
            "success": True,
            "exit_code": 0,
            "stdout": f"Executed: {command}\n",
            "stderr": "",
            "execution_time": 0.05,
            "working_directory": working_dir or "/current/path",
            "environment": env_vars or {}
        }

def file_operation(
    operation: str,
    path: str,
    destination: Optional[str] = None,
    content: Optional[str] = None,
    mode: Optional[str] = None
) -> Dict[str, Any]:
    """
    Simulates file operations (read, write, copy, move, delete)
    
    Args:
        operation: Operation type ('read', 'write', 'copy', 'move', 'delete')
        path: Path to the file
        destination: Destination path for copy/move operations
        content: Content to write for write operation
        mode: File mode for read/write operations
    """
    def validate_path(p: str) -> bool:
        return not any(c in p for c in ['../', '~/', '*', '?'])
    
    # Validate inputs
    if not operation or not path:
        return {
            "success": False,
            "error": "Operation and path are required",
            "error_code": "EINVAL"
        }
    
    # Path safety check
    if not validate_path(path):
        return {
            "success": False,
            "error": "Invalid or unsafe path",
            "error_code": "EINVAL"
        }
    
    current_time = time.time()
    
    # Simulate different operations
    if operation == "read":
        return {
            "success": True,
            "content": "Sample file content\nSecond line\nThird line\n",
            "size": 35,
            "access_time": current_time,
            "modify_time": current_time - 3600,
            "create_time": current_time - 86400
        }
    
    elif operation == "write":
        if not content:
            return {
                "success": False,
                "error": "Content is required for write operation",
                "error_code": "EINVAL"
            }
        return {
            "success": True,
            "bytes_written": len(content),
            "modify_time": current_time,
            "path": path
        }
    
    elif operation in ["copy", "move"]:
        if not destination:
            return {
                "success": False,
                "error": f"Destination path is required for {operation} operation",
                "error_code": "EINVAL"
            }
        if not validate_path(destination):
            return {
                "success": False,
                "error": "Invalid or unsafe destination path",
                "error_code": "EINVAL"
            }
        return {
            "success": True,
            "source": path,
            "destination": destination,
            "operation_time": current_time,
            "size": 1024  # simulated file size
        }
    
    elif operation == "delete":
        return {
            "success": True,
            "path": path,
            "operation_time": current_time
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown operation: {operation}",
            "error_code": "EINVAL"
        }

def system_info() -> Dict[str, Any]:
    """
    Simulates retrieving system information
    """
    return {
        "hostname": "host-1234",
        "os": {
            "platform": "linux",
            "distribution": "Ubuntu 22.04 LTS",
            "kernel": "5.15.0-1034-aws"
        },
        "cpu": {
            "cores": 4,
            "model": "Intel(R) Xeon(R) CPU @ 2.50GHz",
            "usage": 35.2
        },
        "memory": {
            "total": 16_000_000_000,  # 16GB
            "used": 8_500_000_000,    # 8.5GB
            "free": 7_500_000_000,    # 7.5GB
            "swap": {
                "total": 4_000_000_000,
                "used": 500_000_000
            }
        },
        "disk": {
            "/": {
                "total": 100_000_000_000,  # 100GB
                "used": 45_000_000_000,    # 45GB
                "free": 55_000_000_000     # 55GB
            }
        },
        "network": {
            "interfaces": [
                {
                    "name": "eth0",
                    "ip": "172.31.45.123",
                    "mac": "02:42:ac:11:00:02",
                    "stats": {
                        "rx_bytes": 1_500_000_000,
                        "tx_bytes": 800_000_000
                    }
                }
            ]
        },
        "uptime": 345600,  # 4 days in seconds
        "processes": 234,
        "users": 3,
        "timestamp": time.time()
    }

def process_management(
    operation: str,
    pid: Optional[int] = None,
    name: Optional[str] = None,
    signal: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulates process management operations
    
    Args:
        operation: Operation type ('list', 'kill', 'info')
        pid: Process ID for specific operations
        name: Process name for filtering
        signal: Signal number for kill operation
    """
    current_time = time.time()
    
    if operation == "list":
        return {
            "success": True,
            "processes": [
                {
                    "pid": 1,
                    "name": "systemd",
                    "user": "root",
                    "cpu": 0.1,
                    "memory": 0.5,
                    "state": "S",
                    "start_time": current_time - 86400
                },
                {
                    "pid": 1234,
                    "name": "nginx",
                    "user": "www-data",
                    "cpu": 1.5,
                    "memory": 2.3,
                    "state": "S",
                    "start_time": current_time - 3600
                }
            ]
        }
    
    elif operation == "kill":
        if not pid:
            return {
                "success": False,
                "error": "PID is required for kill operation",
                "error_code": "EINVAL"
            }
        return {
            "success": True,
            "pid": pid,
            "signal": signal or 15,  # SIGTERM by default
            "timestamp": current_time
        }
    
    elif operation == "info":
        if not pid and not name:
            return {
                "success": False,
                "error": "Either PID or process name is required",
                "error_code": "EINVAL"
            }
        return {
            "success": True,
            "process": {
                "pid": pid or 1234,
                "name": name or "sample-process",
                "state": "S",
                "user": "ubuntu",
                "group": "ubuntu",
                "priority": 20,
                "nice": 0,
                "threads": 4,
                "cpu_time": 125.3,
                "memory": {
                    "rss": 1024000,
                    "vms": 2048000
                },
                "io": {
                    "read_bytes": 1024000,
                    "write_bytes": 512000
                },
                "start_time": current_time - 3600,
                "cmdline": "/usr/bin/sample-process --config /etc/sample.conf"
            }
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown operation: {operation}",
            "error_code": "EINVAL"
        }

def git_operation(
    operation: str,
    repository_path: str,
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulates Git operations
    
    Args:
        operation: Git operation type (clone/pull/push/commit/status etc.)
        repository_path: Path to git repository
        args: Additional arguments for specific operations
    """
    current_time = time.time()
    
    # Common git status simulation
    def get_git_status() -> Dict[str, Any]:
        return {
            "branch": "main",
            "clean": False,
            "changes": {
                "staged": [
                    {"file": "src/main.py", "status": "modified"},
                    {"file": "docs/README.md", "status": "added"}
                ],
                "unstaged": [
                    {"file": "tests/test_api.py", "status": "modified"},
                    {"file": "config.json", "status": "deleted"}
                ],
                "untracked": [
                    "temp/log.txt",
                    "build/output.bin"
                ]
            }
        }

    # Operation handlers
    if operation == "clone":
        if not args or "url" not in args:
            return {
                "success": False,
                "error": "Repository URL is required for clone operation",
                "error_code": "EINVAL"
            }
        
        return {
            "success": True,
            "operation": "clone",
            "repository": args["url"],
            "destination": repository_path,
            "commit_hash": "a1b2c3d4e5f6g7h8i9j0",
            "branch": "main",
            "time_taken": 3.5
        }
    
    elif operation == "pull":
        return {
            "success": True,
            "operation": "pull",
            "changes": {
                "files_changed": 3,
                "insertions": 45,
                "deletions": 12
            },
            "updated_files": [
                "src/api/endpoints.py",
                "tests/test_utils.py",
                "README.md"
            ],
            "current_commit": "f1e2d3c4b5a6789",
            "previous_commit": "a1b2c3d4e5f6g7h8"
        }
    
    elif operation == "push":
        if not args or "branch" not in args:
            args = {"branch": "main"}  # default branch
            
        return {
            "success": True,
            "operation": "push",
            "branch": args["branch"],
            "remote": "origin",
            "commits_pushed": 2,
            "commit_hashes": [
                "a1b2c3d4e5f6g7h8",
                "b2c3d4e5f6g7h8i9"
            ]
        }
    
    elif operation == "commit":
        if not args or "message" not in args:
            return {
                "success": False,
                "error": "Commit message is required",
                "error_code": "EINVAL"
            }
            
        return {
            "success": True,
            "operation": "commit",
            "commit_hash": "d4e5f6g7h8i9j0k1",
            "message": args["message"],
            "author": "User <user@example.com>",
            "timestamp": current_time,
            "changes": {
                "files_changed": 2,
                "insertions": 25,
                "deletions": 8
            }
        }
    
    elif operation == "status":
        return {
            "success": True,
            "operation": "status",
            "repository": repository_path,
            "status": get_git_status()
        }
    
    elif operation == "log":
        return {
            "success": True,
            "operation": "log",
            "commits": [
                {
                    "hash": "a1b2c3d4e5f6g7h8",
                    "author": "User <user@example.com>",
                    "date": current_time - 3600,
                    "message": "Update API documentation",
                    "changed_files": ["docs/api.md", "src/api/views.py"]
                },
                {
                    "hash": "b2c3d4e5f6g7h8i9",
                    "author": "User <user@example.com>",
                    "date": current_time - 7200,
                    "message": "Fix login bug",
                    "changed_files": ["src/auth/login.py"]
                }
            ]
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown git operation: {operation}",
            "error_code": "EINVAL"
        }

def docker_operation(
    operation: str,
    target: str,
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulates Docker operations
    
    Args:
        operation: Docker operation type (run/build/pull/push/ps etc.)
        target: Container/image name or ID
        args: Additional arguments for specific operations
    """
    current_time = time.time()
    
    if operation == "run":
        if not args:
            args = {}
            
        container_id = str(uuid.uuid4())[:12]
        return {
            "success": True,
            "operation": "run",
            "container_id": container_id,
            "image": target,
            "status": "running",
            "ports": args.get("ports", {}),
            "environment": args.get("environment", {}),
            "volumes": args.get("volumes", []),
            "network": args.get("network", "bridge"),
            "created_at": current_time
        }
    
    elif operation == "build":
        if not args or "dockerfile" not in args:
            return {
                "success": False,
                "error": "Dockerfile path is required for build operation",
                "error_code": "EINVAL"
            }
            
        return {
            "success": True,
            "operation": "build",
            "image": target,
            "tag": args.get("tag", "latest"),
            "steps_completed": 5,
            "build_time": 45.3,
            "size": 856_000_000,  # 856MB
            "layers": [
                {
                    "id": "sha256:a1b2c3d4e5f6...",
                    "size": 125_000_000,
                    "command": "FROM python:3.9-slim"
                },
                {
                    "id": "sha256:b2c3d4e5f6g7...",
                    "size": 250_000,
                    "command": "COPY requirements.txt ."
                }
            ]
        }
    
    elif operation == "ps":
        return {
            "success": True,
            "operation": "ps",
            "containers": [
                {
                    "id": "abc123def456",
                    "image": "python:3.9",
                    "command": "python app.py",
                    "created": current_time - 3600,
                    "status": "Up 1 hour",
                    "ports": {"8080/tcp": 8080},
                    "names": ["web-app"]
                },
                {
                    "id": "def456ghi789",
                    "image": "postgres:13",
                    "command": "postgres",
                    "created": current_time - 7200,
                    "status": "Up 2 hours",
                    "ports": {"5432/tcp": 5432},
                    "names": ["database"]
                }
            ]
        }
    
    elif operation == "logs":
        return {
            "success": True,
            "operation": "logs",
            "container": target,
            "logs": [
                {
                    "timestamp": current_time - 60,
                    "stream": "stdout",
                    "message": "Server started on port 8080"
                },
                {
                    "timestamp": current_time - 30,
                    "stream": "stderr",
                    "message": "Warning: Database connection slow"
                }
            ]
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown docker operation: {operation}",
            "error_code": "EINVAL"
        }

def package_operation(
    operation: str,
    package_name: str,
    manager: str = "pip",
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulates package manager operations (pip, npm, etc.)
    
    Args:
        operation: Operation type (install/uninstall/update/list)
        package_name: Name of the package
        manager: Package manager to use
        args: Additional arguments for specific operations
    """
    if manager not in ["pip", "npm", "yarn"]:
        return {
            "success": False,
            "error": f"Unsupported package manager: {manager}",
            "error_code": "EINVAL"
        }
    
    if operation == "install":
        version = args.get("version") if args else None
        return {
            "success": True,
            "operation": "install",
            "package": package_name,
            "version": version or "1.2.3",
            "manager": manager,
            "dependencies": [
                {"name": "dep1", "version": "0.1.0"},
                {"name": "dep2", "version": "2.0.0"}
            ],
            "installation_path": f"/usr/local/lib/python3.8/site-packages/{package_name}"
                if manager == "pip" else f"node_modules/{package_name}",
            "time_taken": 2.5
        }
    
    elif operation == "uninstall":
        return {
            "success": True,
            "operation": "uninstall",
            "package": package_name,
            "manager": manager,
            "removed_files": 15,
            "freed_space": 1024000,  # 1MB
            "removed_dependencies": [
                "dep1",
                "dep2"
            ]
        }
    
    elif operation == "list":
        return {
            "success": True,
            "operation": "list",
            "manager": manager,
            "packages": [
                {
                    "name": "requests",
                    "version": "2.26.0",
                    "location": "/usr/local/lib/python3.8/site-packages"
                },
                {
                    "name": "django",
                    "version": "3.2.5",
                    "location": "/usr/local/lib/python3.8/site-packages"
                }
            ] if manager == "pip" else [
                {
                    "name": "express",
                    "version": "4.17.1",
                    "location": "node_modules/express"
                },
                {
                    "name": "react",
                    "version": "17.0.2",
                    "location": "node_modules/react"
                }
            ]
        }
    
    elif operation == "search":
        return {
            "success": True,
            "operation": "search",
            "query": package_name,
            "manager": manager,
            "results": [
                {
                    "name": package_name,
                    "version": "1.2.3",
                    "description": "Sample package description",
                    "downloads": 1000000,
                    "homepage": f"https://example.com/{package_name}",
                    "repository": f"https://github.com/example/{package_name}"
                }
            ]
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown operation: {operation}",
            "error_code": "EINVAL"
        }

def http_request(
    url: str,
    method: str = "GET",
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[str, Dict[str, Any]]] = None,
    timeout: int = 30,
    follow_redirects: bool = True,
    verify_ssl: bool = True
) -> Dict[str, Any]:
    """
    Simulates HTTP requests (curl/wget like functionality)
    
    Args:
        url: Target URL
        method: HTTP method
        headers: Request headers
        data: Request body data
        timeout: Request timeout in seconds
        follow_redirects: Whether to follow redirects
        verify_ssl: Whether to verify SSL certificates
    """
    def validate_url(url: str) -> bool:
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
            
    def simulate_response_time() -> float:
        # Simulate network latency (50-500ms)
        return random.uniform(0.05, 0.5)
    
    # Validate URL
    if not validate_url(url):
        return {
            "success": False,
            "error": "Invalid URL format",
            "error_code": "EINVAL",
            "curl_error": 3  # CURLE_URL_MALFORMAT
        }
    
    response_time = simulate_response_time()
    current_time = time.time()
    
    # Simulate common HTTP scenarios
    if "example.com" in url:
        return {
            "success": True,
            "status_code": 200,
            "headers": {
                "content-type": "application/json",
                "server": "nginx/1.18.0",
                "date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime(current_time)),
                "content-length": "1234"
            },
            "body": "<!DOCTYPE html><html><body><h1>Example Domain</h1></body></html>",
            "response_time": response_time,
            "redirect_count": 0,
            "size_downloaded": 1234,
            "speed_download": 1234 / response_time
        }
    elif "nonexistent" in url:
        return {
            "success": False,
            "status_code": 404,
            "error": "Not Found",
            "response_time": response_time
        }
    else:
        return {
            "success": True,
            "status_code": 200,
            "headers": headers or {},
            "body": "Simulated response body",
            "response_time": response_time
        }

def network_diagnostic(
    target: str,
    operation: str,
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulates network diagnostic tools (ping, traceroute, nslookup, etc.)
    
    Args:
        target: Target host/IP
        operation: Diagnostic operation type
        args: Additional arguments for the operation
    """
    current_time = time.time()
    
    if operation == "ping":
        packet_loss = random.uniform(0, 0.1)  # 0-10% packet loss
        return {
            "success": True,
            "operation": "ping",
            "target": target,
            "statistics": {
                "packets_transmitted": 4,
                "packets_received": int(4 * (1 - packet_loss)),
                "packet_loss_percent": packet_loss * 100,
                "round_trip_times": {
                    "min": 15.3,
                    "avg": 28.7,
                    "max": 35.1,
                    "mdev": 8.2
                }
            },
            "raw_output": [
                f"PING {target} (93.184.216.34) 56(84) bytes of data.",
                f"64 bytes from {target} (93.184.216.34): icmp_seq=1 ttl=56 time=28.7 ms",
                f"64 bytes from {target} (93.184.216.34): icmp_seq=2 ttl=56 time=15.3 ms",
                f"64 bytes from {target} (93.184.216.34): icmp_seq=3 ttl=56 time=35.1 ms",
                f"64 bytes from {target} (93.184.216.34): icmp_seq=4 ttl=56 time=31.2 ms"
            ]
        }
    
    elif operation == "traceroute":
        return {
            "success": True,
            "operation": "traceroute",
            "target": target,
            "hops": [
                {
                    "hop": 1,
                    "host": "192.168.1.1",
                    "rtt": [2.1, 2.3, 2.2]
                },
                {
                    "hop": 2,
                    "host": "10.0.0.1",
                    "rtt": [5.1, 5.4, 5.2]
                },
                {
                    "hop": 3,
                    "host": "93.184.216.34",
                    "rtt": [15.3, 15.1, 15.4]
                }
            ],
            "total_hops": 3,
            "time_taken": 0.45
        }
    
    elif operation == "nslookup":
        return {
            "success": True,
            "operation": "nslookup",
            "target": target,
            "results": {
                "name": target,
                "addresses": ["93.184.216.34", "2606:2800:220:1:248:1893:25c8:1946"],
                "aliases": [],
                "nameservers": [
                    {"host": "ns1.example.com", "address": "198.51.100.1"},
                    {"host": "ns2.example.com", "address": "198.51.100.2"}
                ]
            },
            "query_time": 0.12
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown diagnostic operation: {operation}",
            "error_code": "EINVAL"
        }

def ssh_operation(
    operation: str,
    host: str,
    username: str,
    args: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Simulates SSH operations (connect, execute command, transfer file)
    
    Args:
        operation: SSH operation type
        host: Target host
        username: Username for authentication
        args: Additional arguments (password, key_file, commands, etc.)
    """
    current_time = time.time()
    
    if operation == "connect":
        # Simulate SSH connection
        return {
            "success": True,
            "operation": "connect",
            "connection_info": {
                "host": host,
                "username": username,
                "connected_at": current_time,
                "session_id": f"ssh_{random.randint(1000, 9999)}",
                "client_version": "SSH-2.0-OpenSSH_8.2p1",
                "server_version": "SSH-2.0-OpenSSH_7.6p1",
                "encryption": "aes256-ctr",
                "mac": "hmac-sha2-256"
            }
        }
    
    elif operation == "execute":
        if not args or "command" not in args:
            return {
                "success": False,
                "error": "Command is required for execute operation",
                "error_code": "EINVAL"
            }
            
        return {
            "success": True,
            "operation": "execute",
            "command": args["command"],
            "output": {
                "stdout": "Command output simulation\nLine 2 of output",
                "stderr": "",
                "exit_code": 0
            },
            "execution_time": 0.23
        }
    
    elif operation == "scp_upload":
        if not args or "local_path" not in args or "remote_path" not in args:
            return {
                "success": False,
                "error": "Both local and remote paths are required for SCP upload",
                "error_code": "EINVAL"
            }
            
        return {
            "success": True,
            "operation": "scp_upload",
            "transfer_info": {
                "local_path": args["local_path"],
                "remote_path": args["remote_path"],
                "bytes_transferred": 1024000,
                "speed": 2048000,  # 2MB/s
                "time_taken": 0.5
            }
        }
    
    elif operation == "scp_download":
        if not args or "remote_path" not in args or "local_path" not in args:
            return {
                "success": False,
                "error": "Both remote and local paths are required for SCP download",
                "error_code": "EINVAL"
            }
            
        return {
            "success": True,
            "operation": "scp_download",
            "transfer_info": {
                "remote_path": args["remote_path"],
                "local_path": args["local_path"],
                "bytes_transferred": 2048000,
                "speed": 4096000,  # 4MB/s
                "time_taken": 0.5
            }
        }
    
    else:
        return {
            "success": False,
            "error": f"Unknown SSH operation: {operation}",
            "error_code": "EINVAL"
        }

def network_info() -> Dict[str, Any]:
    """
    Retrieves network interface and routing information
    """
    return {
        "interfaces": [
            {
                "name": "eth0",
                "ip_address": "192.168.1.100",
                "netmask": "255.255.255.0",
                "mac_address": "00:11:22:33:44:55",
                "status": "up",
                "mtu": 1500,
                "statistics": {
                    "rx_bytes": 1500000,
                    "tx_bytes": 500000,
                    "rx_packets": 1200,
                    "tx_packets": 800,
                    "errors": 0,
                    "dropped": 0
                }
            },
            {
                "name": "wlan0",
                "ip_address": "192.168.1.101",
                "netmask": "255.255.255.0",
                "mac_address": "AA:BB:CC:DD:EE:FF",
                "status": "up",
                "mtu": 1500,
                "wireless": {
                    "ssid": "MyNetwork",
                    "signal_strength": -65,  # dBm
                    "frequency": "2.4GHz",
                    "encryption": "WPA2"
                }
            }
        ],
        "routing_table": [
            {
                "destination": "0.0.0.0",
                "gateway": "192.168.1.1",
                "netmask": "0.0.0.0",
                "interface": "eth0",
                "metric": 100
            },
            {
                "destination": "192.168.1.0",
                "gateway": "0.0.0.0",
                "netmask": "255.255.255.0",
                "interface": "eth0",
                "metric": 0
            }
        ],
        "dns_servers": [
            "8.8.8.8",
            "8.8.4.4"
        ],
        "hostname": "myhost",
        "domain": "local"
    }