// 调试导入功能的工具函数

export const debugExcelParsing = () => {
  console.log('=== Excel解析调试信息 ===')
  console.log('XLSX库状态:', typeof XLSX !== 'undefined' ? '已加载' : '未加载')
  
  if (typeof XLSX !== 'undefined') {
    console.log('XLSX版本:', XLSX.version)
    console.log('可用方法:', Object.keys(XLSX))
  }
  
  console.log('FileReader支持:', typeof FileReader !== 'undefined' ? '是' : '否')
  console.log('Blob支持:', typeof Blob !== 'undefined' ? '是' : '否')
  console.log('ArrayBuffer支持:', typeof ArrayBuffer !== 'undefined' ? '是' : '否')
  console.log('Uint8Array支持:', typeof Uint8Array !== 'undefined' ? '是' : '否')
}

export const createTestExcelData = () => {
  if (typeof XLSX === 'undefined') {
    console.error('XLSX库未加载')
    return null
  }
  
  try {
    // 创建测试数据
    const testData = [
      ['科目ID', '科目名称', '题型', '题目', '内容', '选项', '答案', '解析', '难度', '标签', '分值', '状态'],
      ['1', 'Python编程', 'single', '测试题目', '测试内容', 'A|B|C|D', 'A', '测试解析', 'easy', '测试|标签', '1', 'draft']
    ]
    
    // 创建工作簿
    const wb = XLSX.utils.book_new()
    const ws = XLSX.utils.aoa_to_sheet(testData)
    XLSX.utils.book_append_sheet(wb, ws, '试题模板')
    
    // 转换为二进制数据
    const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' })
    
    return wbout
  } catch (error) {
    console.error('创建测试Excel数据失败:', error)
    return null
  }
}

export const testExcelParsing = (file) => {
  return new Promise((resolve, reject) => {
    if (typeof XLSX === 'undefined') {
      reject(new Error('XLSX库未加载'))
      return
    }
    
    const reader = new FileReader()
    
    reader.onload = (e) => {
      try {
        console.log('文件读取成功，开始解析...')
        const data = new Uint8Array(e.target.result)
        const workbook = XLSX.read(data, { type: 'array' })
        
        console.log('工作簿信息:', {
          sheetNames: workbook.SheetNames,
          sheets: Object.keys(workbook.Sheets)
        })
        
        const sheetName = workbook.SheetNames[0]
        const worksheet = workbook.Sheets[sheetName]
        const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 })
        
        console.log('解析结果:', jsonData)
        
        resolve({
          workbook,
          sheetName,
          worksheet,
          jsonData
        })
      } catch (error) {
        console.error('Excel解析失败:', error)
        reject(error)
      }
    }
    
    reader.onerror = (error) => {
      console.error('文件读取失败:', error)
      reject(error)
    }
    
    reader.readAsArrayBuffer(file)
  })
}
