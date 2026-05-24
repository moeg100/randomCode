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
