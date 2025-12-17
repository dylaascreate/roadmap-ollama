# Test Query Notes
```
// 1. Check Skill Dependencies (Locked vs Safe)
SELECT 
    s.id, 
    s.name, 
    COUNT(su.user_id) as user_count,
    CASE WHEN COUNT(su.user_id) > 0 THEN 'LOCKED 🔒' ELSE 'SAFE ✅' END as status
FROM skills s
LEFT JOIN skill_user su ON s.id = su.skill_id
GROUP BY s.id, s.name;
```
```
// 2. Check Career Dependencies
SELECT 
    c.id, 
    c.name, 
    COUNT(u.id) as user_count,
    CASE WHEN COUNT(u.id) > 0 THEN 'LOCKED 🔒' ELSE 'SAFE ✅' END as status
FROM careers c
LEFT JOIN users u ON c.id = u.career_id
GROUP BY c.id, c.name;
```
```
// 3. The "Who is it?" Query (Deep Dive)
SELECT 
    u.id as user_id, 
    u.name as user_name, 
    s.name as skill_name
FROM users u
JOIN skill_user su ON u.id = su.user_id
JOIN skills s ON su.skill_id = s.id
ORDER BY s.name;

```
Testing Strategy:
1. Run Query 1. Find a skill with LOCKED status.
2. Try to delete it in Postman. -> Expect Error.
3. Find a skill with SAFE status.
4. Try to delete it in Postman. -> Expect Success.

### Run this whenever the code looks messy:
```
# Laravel/pint
./vendor/bin/pint
```
