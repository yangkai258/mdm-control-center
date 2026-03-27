import re

router_path = 'C:/Users/YKing/.openclaw/workspace/mdm-project/frontend/src/router/index.js'

with open(router_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the routes array
routes_match = re.search(r'const routes = \[(.*?)\n]', content, re.DOTALL)
if not routes_match:
    print("Could not find routes")
    exit(1)

routes_content = routes_match.group(1)

# Parse routes - split by finding top-level route objects
# Each route starts with whitespace followed by { and ends with },
# But we need to handle nested braces properly

routes = []
depth = 0
in_string = False
string_char = None
current = ""
i = 0

while i < len(routes_content):
    c = routes_content[i]
    
    # Handle strings
    if c in '"\'':
        if i == 0 or routes_content[i-1] != '\\':
            if not in_string:
                in_string = True
                string_char = c
            elif c == string_char:
                in_string = False
                string_char = None
    
    if not in_string:
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
        
        # At depth 0, when we see a comma followed by newline and whitespace and {
        if depth == 0 and c == ',':
            next_i = i + 1
            while next_i < len(routes_content) and routes_content[next_i] in ' \t\n':
                next_i += 1
            if next_i < len(routes_content) and routes_content[next_i] == '{':
                routes.append((current + ',').strip())
                current = ""
                i = next_i
                continue
    
    current += c
    i += 1

if current.strip():
    routes.append(current.strip())

print(f"Found {len(routes)} routes")

# Categorize routes
login_routes = []
child_routes = []

for route in routes:
    # Check if this is a login route
    if "'/login'" in route or "'/test-modals'" in route:
        login_routes.append(route)
    elif "'/'" in route and "'redirect'" in route:
        # Root redirect - modify path
        modified = re.sub(r"path: '/'", "path: '/'", route)
        child_routes.append(modified)
    else:
        # Modify path to remove leading /
        modified = route
        modified = re.sub(r"path: '/", "path: '", modified)
        modified = re.sub(r"redirect: '/", "redirect: '", modified)
        child_routes.append(modified)

print(f"Login routes: {len(login_routes)}")
print(f"Child routes: {len(child_routes)}")

# Build new routes content
lines = []
lines.append("import { createRouter, createWebHistory } from 'vue-router'")
lines.append("")
lines.append("const routes = [")

# Add login routes first (with commas)
for i, route in enumerate(login_routes):
    if not route.endswith(','):
        route = route + ','
    lines.append(route)

# Add parent route with layout
lines.append("  {")
lines.append("    path: '/',")
lines.append("    component: () => import('../layout/index.vue'),")
lines.append("    children: [")

# Add child routes (with proper commas)
for i, route in enumerate(child_routes):
    # Ensure trailing comma
    if not route.endswith(','):
        route = route + ','
    lines.append("      " + route)

# Close children and parent
lines.append("    ]")
lines.append("  }")
lines.append("]")

# Add router creation and guards
lines.append("")
lines.append("const router = createRouter({")
lines.append("  history: createWebHistory(),")
lines.append("  routes")
lines.append("})")
lines.append("")
lines.append("// 路由守卫：检查登录状态")
lines.append("router.beforeEach((to, from, next) => {")
lines.append("  const token = localStorage.getItem('token')")
lines.append("  ")
lines.append("  // 如果访问登录页面，直接放行")
lines.append("  if (to.path === '/login') {")
lines.append("    if (token) {")
lines.append("      next('/dashboard')")
lines.append("    } else {")
lines.append("      next()")
lines.append("    }")
lines.append("    return")
lines.append("  }")
lines.append("  ")
lines.append("  // 其他页面需要登录")
lines.append("  if (!token) {")
lines.append("    next('/login')")
lines.append("    return")
lines.append("  }")
lines.append("  ")
lines.append("  next()")
lines.append("})")
lines.append("")
lines.append("export default router")

# Write new file
with open(router_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Router fixed!")
