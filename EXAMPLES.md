# 示例

这里用接近真实工作的代码示例说明四条原则。每个示例都展示 LLM 常见的错误做法，以及更合适的处理方式。

---

## 1. 编码前先思考

### 示例 1：隐藏假设

**用户请求：** “添加一个导出用户数据的功能”

**❌ LLM 常见错误做法：直接带着错误假设实现**

```python
def export_users(format='json'):
    """Export all users to a file."""
    users = User.query.all()
    
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    
    return f"Exported {len(users)} users"
```

**问题：**
- 假设要导出所有用户，没有确认分页、权限和隐私边界。
- 假设输出文件位置，没有询问。
- 假设字段范围，没有确认哪些字段可导出。
- 假设 CSV 字段名，没有检查真实数据结构。

**✅ 更合适的做法：先暴露假设**

```text
实现前我需要先确认几个点：

1. **范围**：导出所有用户，还是导出筛选后的用户？这涉及隐私和权限。
2. **形式**：你说的“导出”是指：
   - 浏览器下载文件？
   - 后台任务生成文件并邮件通知？
   - API endpoint 直接返回数据？
3. **字段**：需要导出哪些 user fields？有些字段可能敏感。
4. **数据量**：通常有多少用户？这会影响实现方式。

最简单的方案是：添加一个返回分页 JSON 的 API endpoint。
如果需要文件导出，还需要确认更多细节。

你更倾向哪种方式？
```

### 示例 2：多种解释

**用户请求：** “让搜索更快”

**❌ LLM 常见错误做法：默默选择一种解释**

```python
# Adds caching, database indexes, and async processing
# without asking which "faster" matters
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # ... 200 lines of optimization code
```

**✅ 更合适的做法**

```text
“让搜索更快”可能指几件不同的事：

1. **响应时间更短**，比如从 500ms 降到 100ms 以内
   - 添加 database indexes
   - 缓存高频查询
   - 预计工作量：2 小时

2. **支持更多并发搜索**，也就是提升 throughput
   - 引入 async/await
   - 调整 connection pooling
   - 预计工作量：4 小时

3. **感知速度更快**，也就是改善 UX
   - 先展示部分结果
   - progressive loading
   - 预计工作量：3 小时

目前典型搜索耗时大约 500ms。
你最关心哪一类“更快”？
```

---

## 2. 简洁优先

### 示例 1：过度抽象

**用户请求：** “添加一个计算折扣的函数”

**❌ LLM 常见错误做法：过度设计**

```python
from abc import ABC, abstractmethod
from enum import Enum
from typing import Protocol, Union
from dataclasses import dataclass

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        self.percentage = percentage
    
    def calculate(self, amount: float) -> float:
        return amount * (self.percentage / 100)

class FixedDiscount(DiscountStrategy):
    def __init__(self, fixed_amount: float):
        self.fixed_amount = fixed_amount
    
    def calculate(self, amount: float) -> float:
        return min(self.fixed_amount, amount)

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig):
        self.config = config
    
    def apply_discount(self, amount: float) -> float:
        if amount < self.config.min_purchase:
            return 0
        discount = self.config.strategy.calculate(amount)
        return min(discount, self.config.max_discount)

# Usage requires 30+ lines of setup for a simple calculation
```

**✅ 更合适的做法：先保持简单**

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)

# Usage
discount = calculate_discount(100.0, 10.0)  # $10 off
```

**什么时候增加复杂度：** 只有在真的需要多种 discount types 时再引入抽象。如果需求之后出现，再重构也不晚。

### 示例 2：提前添加功能

**用户请求：** “把用户偏好保存到数据库”

**❌ LLM 常见错误做法：实现用户没要求的能力**

```python
class PreferenceManager:
    def __init__(self, db, cache=None, validator=None):
        self.db = db
        self.cache = cache or InMemoryCache()
        self.validator = validator or DefaultValidator()
    
    def save(self, user_id: int, prefs: dict, 
             merge: bool = True, 
             validate: bool = True,
             notify: bool = False) -> bool:
        """Save preferences with optional merging, validation, and notifications."""
        
        if validate:
            errors = self.validator.validate(prefs)
            if errors:
                raise ValidationError(errors)
        
        existing = self.get(user_id) if merge else {}
        
        if merge:
            existing.update(prefs)
            prefs = existing
        
        self.db.execute(
            "UPDATE users SET preferences = ? WHERE id = ?",
            (json.dumps(prefs), user_id)
        )
        
        if self.cache:
            self.cache.set(f"prefs:{user_id}", prefs)
        
        if notify:
            self.notify_preference_change(user_id, prefs)
        
        return True
    
    def notify_preference_change(self, user_id: int, prefs: dict):
        # Another 30 lines for a feature nobody asked for
        pass
```

**✅ 更合适的做法：只做被要求的事**

```python
def save_preferences(db, user_id: int, preferences: dict):
    """Save user preferences to database."""
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

**之后再加也不迟：** 性能真的有问题时再加 caching；出现坏数据时再加 validation；需求明确时再加 merging。

---

## 3. 精准修改

### 示例 1：顺手重构

**用户请求：** “修复空 email 会导致 validator 崩溃的问题”

**❌ LLM 常见错误做法：改得太多**

```diff
  def validate_user(user_data):
-     # Check email format
-     if not user_data.get('email'):
+     """Validate user data."""
+     email = user_data.get('email', '').strip()
+     
+     # Validate email
+     if not email:
          raise ValueError("Email required")
-     
-     # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
      
-     # Check username
-     if not user_data.get('username'):
+     # Validate username
+     username = user_data.get('username', '').strip()
+     if not username:
          raise ValueError("Username required")
+     if len(username) < 3:
+         raise ValueError("Username too short")
+     if not username.isalnum():
+         raise ValueError("Username must be alphanumeric")
      
      return True
```

**问题：**
- 在修 bug 的同时“改进”了 email validation。
- 添加了用户没有要求的 username validation。
- 改了注释。
- 添加了 docstring。

**✅ 更合适的做法：精准修改**

```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
      
      # Check username
      if not user_data.get('username'):
          raise ValueError("Username required")
      
      return True
```

**只改变：** 修复空 email 处理所必需的几行。

### 示例 2：风格漂移

**用户请求：** “给 upload function 添加 logging”

**❌ LLM 常见错误做法：顺手重排所有东西**

```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
+     logger.info(f"Uploading {file_path} to {destination}")
+     
      try:
-         with open(file_path, 'rb') as f:
-             data = f.read()
-         
-         response = requests.post(destination, files={'file': data})
-         
-         if response.status_code == 200:
-             return True
-         else:
-             return False
+         with open(file_path, "rb") as f:
+             data = f.read()
+         response = requests.post(destination, files={"file": data})
+         success = response.status_code == 200
+         
+         if success:
+             logger.info(f"Upload successful: {file_path}")
+         else:
+             logger.error(f"Upload failed: {file_path}, status={response.status_code}")
+         
+         return success
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f"Upload error for {file_path}: {e}")
          return False
```

**问题：**
- 把单引号改成了双引号。
- 添加了用户没有要求的 type hints。
- 添加了 docstring。
- 改了空行和排版。
- 改写了 boolean return 逻辑。

**✅ 更合适的做法：匹配现有风格**

```diff
+ import logging
+ 
+ logger = logging.getLogger(__name__)
+ 
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
          with open(file_path, 'rb') as f:
              data = f.read()
          
          response = requests.post(destination, files={'file': data})
          
          if response.status_code == 200:
+             logger.info(f'Upload successful: {file_path}')
              return True
          else:
+             logger.error(f'Upload failed: {file_path}, status={response.status_code}')
              return False
      except Exception as e:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
          return False
```

**匹配现有代码：** 单引号、无 type hints、保留原有 boolean pattern、保留原有 spacing style。

---

## 4. 目标驱动执行

### 示例 1：模糊目标 vs. 可验证目标

**用户请求：** “修复 authentication system”

**❌ LLM 常见错误做法：计划很空泛**

```text
我会这样修复 authentication system：
1. 阅读代码
2. 找出问题
3. 做一些改进
4. 测试改动

[随后在没有明确成功标准的情况下直接修改]
```

**✅ 更合适的做法：定义可验证目标**

```text
“修复 authentication”需要先定义成功标准。
我们具体要解决哪个问题？

如果问题是“用户修改密码后旧 session 仍然有效”：

计划：
1. 写测试：修改密码 -> 验证旧 session 失效
   验证：测试失败，并且能复现 bug

2. 实现：修改密码时 invalidate sessions
   验证：测试通过

3. 检查边界情况：多个 active sessions、并发修改
   验证：补充测试通过

4. 验证无回归：现有 auth tests 仍然通过
   验证：完整 test suite green

当前 auth test coverage：[展示 coverage]
你实际遇到的 authentication 问题是哪一个？
```

### 示例 2：多步骤任务也要逐步验证

**用户请求：** “给 API 添加 rate limiting”

**❌ LLM 常见错误做法：一次性做完所有东西**

```python
# Implements full rate limiting with Redis, multiple strategies,
# configuration system, and monitoring in one 300-line commit
# No clear verification steps
```

**✅ 更合适的做法：分步实现并验证**

```text
rate limiting 的计划：

1. 添加基础 in-memory rate limiting，先覆盖单个 endpoint
   验证：
   - 测试：100 个请求 -> 前 10 个成功，其余返回 429
   - 手动：curl endpoint 11 次，看到 rate limit error

2. 提取成 middleware，应用到所有 endpoints
   验证：
   - 测试：rate limits 同时作用于 /users 和 /posts
   - 现有 endpoint tests 仍然通过

3. 添加 Redis backend，用于 multi-server 场景
   验证：
   - 测试：app restart 后 rate limit 仍然符合预期
   - 测试：两个 app instances 共享 rate limit counter

4. 添加配置，支持 per-endpoint rates
   验证：
   - 测试：/search 允许 10/min，/users 允许 100/min
   - config file 能正确解析

每一步都可以独立验证，也可以独立部署。
先从第 1 步开始吗？
```

### 示例 3：测试先行验证

**用户请求：** “sorting 在有重复 scores 时会出问题”

**❌ LLM 常见错误做法：没有复现就直接修**

```python
# Immediately changes sort logic without confirming the bug
def sort_scores(scores):
    return sorted(scores, key=lambda x: (-x['score'], x['name']))
```

**✅ 更合适的做法：先复现问题**

```python
# 1. First, write a test that reproduces the issue
def test_sort_with_duplicate_scores():
    """Test sorting when multiple items have same score."""
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    
    result = sort_scores(scores)
    
    # The bug: order is non-deterministic for duplicates
    # Run this test multiple times, it should be consistent
    assert result[0]['score'] == 100
    assert result[1]['score'] == 100
    assert result[2]['score'] == 90

# Verify: Run test 10 times -> fails with inconsistent ordering

# 2. Now fix with stable sort
def sort_scores(scores):
    """Sort by score descending, then name ascending for ties."""
    return sorted(scores, key=lambda x: (-x['score'], x['name']))

# Verify: Test passes consistently
```

---

## 反模式总结

| 原则 | 反模式 | 修正方式 |
| --- | --- | --- |
| 编码前先思考 | 默默假设文件格式、字段、范围 | 明确列出假设，并请求澄清 |
| 简洁优先 | 为单个折扣计算引入 strategy pattern | 先用一个函数，等复杂度真的出现再抽象 |
| 精准修改 | 修 bug 时顺手改引号、加 type hints、重排格式 | 只改能直接解决问题的行 |
| 目标驱动执行 | “我会 review 并 improve code” | “为 bug X 写测试 -> 让测试通过 -> 验证无回归” |

## 核心洞察

“过度复杂”的示例并不是看起来明显错误。它们往往使用了 design patterns 和所谓 best practices。真正的问题是**时机**：在复杂度真正出现之前，就提前引入复杂度。

这会带来几个后果：

- 代码更难理解。
- bug 面更大。
- 实现时间更长。
- 测试更困难。

简单版本的好处是：

- 更容易理解。
- 更快实现。
- 更容易测试。
- 当复杂度真的出现时，仍然可以重构。

**好代码不是提前解决明天可能出现的问题，而是用简单方式解决今天真实存在的问题。**
