module.exports = async (params) => {
    const { quickAddApi: QuickAdd, app } = params;

    // Lấy tiêu đề từ người dùng
    const title = await QuickAdd.utility.getTemplateVariable('title');

    // Phân tách tiêu đề thành các từ và đếm
    const wordCount = title.trim().split(/\s+/).length;

    // Xác định thư mục và template dựa trên số từ
    let targetFolder, targetTemplate;
    if (wordCount === 1) {
        targetFolder = "20_Vocabulary";
        targetTemplate = "tpl_Vocabulary";
    } else {
        targetFolder = "30_Structures";
        targetTemplate = "tpl_Structure";
    }

    // Thiết lập biến cho template
    QuickAdd.variables.targetFolder = targetFolder;
    QuickAdd.variables.wordCount = wordCount;
    QuickAdd.variables.targetTemplate = targetTemplate;

    return;
}