class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        result = []
        for i in range(len(nums) - 1):
            if len(result) == 0:
                for j in range(len(nums) - 1):
                    if nums[i] + nums[j + 1] == target and i != j+1:
                        result.append(i)
                        result.append(j+1)
                        break
            else:
                break
        return result


sol = Solution()
print(sol.twoSum([2,7,11,15], 9))
print(sol.twoSum([3, 2, 4], 6))
print(sol.twoSum([3,3], 6))
print(sol.twoSum([2,5,5,11], 10))
print(sol.twoSum([3, 2, 3], 6))







# RomanToInt

class Solution:
    def romanToInt(self, s):
        numerical = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    
        total = 0
    
        for i in range(len(s)):
            if i < (len(s) - 1) and numerical[s[i]] < numerical[s[i + 1]]:
                total -= numerical[s[i]]
            else:
                total += numerical[s[i]]
            
        return total

a = Solution()
print(a.romanToInt("IIV"))
