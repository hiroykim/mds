import org.deeplearning4j.nn.modelimport.keras.*;
import org.nd4j.linalg.factory.Nd4j;
import org.deeplearning4j.nn.multilayer.MultiLayerNetwork;
import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4jBackend;


public class TestEnd {

	public static void main(String args[]){
		
		Nd4jBackend b = Nd4j.getBackend();
		System.out.println("Test1");
		if(b!=null){
			System.out.println("Test2");
			boolean gpuBackendAvailable = b.getClass().getCanonicalName().toLowerCase().contains("jcublas");
			System.out.println("Result : " + gpuBackendAvailable);
		}

		try {

            //Nd4j.setDefaultDataTypes(org.nd4j.linalg.api.buffer.DataBuffer.Type.DOUBLE, 
            //                        org.nd4j.linalg.api.buffer.DataBuffer.TypeEx.FLOAT16);
            //Nd4j.setDataType(org.nd4j.linalg.api.buffer.DataBuffer.Type.FLOAT);
            /* 이게 제일 정확도 높았음 */
            //Nd4j.setDataType(org.nd4j.linalg.api.buffer.DataBuffer.Type.DOUBLE);

			MultiLayerNetwork model =
				KerasModelImport.importKerasSequentialModelAndWeights(
                    //"./model/KMV_prediction_201127_archi.json", "./model/KMV_prediction_201127_weight.h5");
                    //"./model/KMV_prediction_210205_archi.json", "./model/KMV_prediction_210205_weight.h5");
                    "./model/KMV_prediction_210302_archi.json", "./model/KMV_prediction_210302_weight.h5");
            if(1==1)
                return;

            /* 인풋매트릭스 생성
             * sbc_amt는 현재는 모든 경우에 -1
             * 딱 한 줄 만드는 버전
             */
             /*
            INDArray input = makeInputSample(
                "61008", "null", "null", 20, 20, "752", "10NP012", 
                60, "1", 1, "UP", "3_1", 
                "610208", -1, 20, 20, 100
                );
            INDArray input = makeInputSample(
                "61334", "null", "null", 20, 20, "705", "10NP010", 
                40, "1", 1, "null", "3_1", 
                "630022", -1, 20, 20, 100
                );
            */

            String test_cov_cd = "610766";
            /*
            INDArray input = makeInputSample
            ("61334", "null", "null", 20, 20, "705", "10NP010", 40, "1", 1, "null", "1_1", "630931", -1, 20, 20, 0);
            */
            INDArray input = makeInputSample
            ("61334", "null", "06", 20, 20, "705", "10NP010", 40, "1", 1, "null", "1_1", test_cov_cd, 30000, 20, 20, 0);
        
            /* input 어레이 상태 */
            showINDArray(input);

            /* 모형 결과 계산 */
            INDArray output = model.output(input);
            /* 모형 결과 조회 */
            double result = output.getDouble(0, 0);

            System.out.println(result);
            System.out.println(Math.signum(result) * (Math.exp(Math.abs(result)*10)-1));

            System.out.println(input.getScalar(0, ModelInfo.common_part_len - 3));
            System.out.println(input.getScalar(0, ModelInfo.common_part_len - 2));
            System.out.println(input.getScalar(0, ModelInfo.common_part_len - 1));
            
            input.putScalar(0, ModelInfo.common_part_len - 3, 1);
            input.putScalar(0, ModelInfo.common_part_len - 2, 0);
            input.putScalar(0, ModelInfo.common_part_len - 1, 0);

            System.out.println(model.output(input).getDouble(0, 0));


            /* cov_list 테스트 */
            /* 담보코드 one-hot */ 
            int testIndex = -1;
            for(int i=0;i<ModelInfo.cov_list1.length;i++){
                if(test_cov_cd.equals(ModelInfo.cov_list1[i])){
                    testIndex = i;
                    break;
                }
            }
            System.out.println("cov_cd = " + test_cov_cd + ", index = " + testIndex);

            System.out.println(ModelInfo.cov_list2[testIndex][0] + ", " + ModelInfo.cov_list2[testIndex][1]);

            

            if(1==1)
                return;



            /* 한번에 여러줄 만들어 계산하는 테스트 */ 
            System.out.println("===== matrix style =====");

            INDArray inputAll = makeInputAllSample(
                "60546", "null", "null", 15, 15, "712", "10NP011",
                24, "2", 1, "null", "1_1");

            showINDArray(inputAll);

            INDArray outputAll = model.output(inputAll);

            for(int i=0;i<outputAll.rows();i++){
                System.out.println(outputAll.getDouble(i, 0));
                ;
            }


            /* 상해등급은 1,2,3,null 등급에 대해 모두 계산하는 요건 있음 */
            /* 일단 현재 상해등급 index는 1등급이 110, 2등급 111, 3등급 112 */
            /* 이 index는 모형 버전바다 바뀔 수 있어 다음과 같이 바꾼다 */
            /* ModelInfo.common_part_len -3, -2, -1  */
            /* 위 사람(1등급)을 2등급 기준으로 계산하는 예 */ 
            System.out.println("===== inspe grade 2 =====");

            for(int i=0;i<inputAll.rows();i++){
                inputAll.putScalar(i, ModelInfo.common_part_len - 3, 0);
                inputAll.putScalar(i, ModelInfo.common_part_len - 2, 1);
                inputAll.putScalar(i, ModelInfo.common_part_len - 1, 0);
            }

            showINDArray(inputAll);


		} catch(Exception e){
			e.printStackTrace();
		}

	}


    /* 
     * python의 _make_feature 함수에 대응
    */
    public static INDArray makeInputSample(
            /* 계약 정보 */
            String rps_pd_cd, String py_exem_tp_cd, String lwrt_tmn_rfd_tp_cd, 
            int ctr_ins_prd, int ctr_py_prd, String fee_pay_tp_cd, String rcrt_bch_org_cd,
            /* 목적물 정보 */
            int sbc_age, String gndr_cd, int injr_gr_num, String plan_cd, String inspe_grde_val, 
            /* 담보 정보 */ 
            String cov_cd, int sbc_amt, int ins_prd, int py_prd, int rnwl_ed_age
            ){

        INDArray input;
        int curIndex = 0;
        int putIndex = -1;

        String[] pd_list = ModelInfo.pd_list;
        String[] exem_list = ModelInfo.exem_list;
        String[] lwrt_list = ModelInfo.lwrt_list;
        String[] fee_list = ModelInfo.fee_list;
        String[] bch_list = ModelInfo.bch_list;
        String[] pl_list = ModelInfo.pl_list;
        String[] cov_list1 = ModelInfo.cov_list1;
        double[][] cov_list2 = ModelInfo.cov_list2;


        input = Nd4j.zeros(1, ModelInfo.input_len);

        /* 상품코드 one-hot */
        for(int i=0;i<pd_list.length;i++){
            if(rps_pd_cd.equals(pd_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += pd_list.length;
        putIndex = -1;


        /* 납입면제유형코드 one-hot */ 
        for(int i=0;i<exem_list.length;i++){
            if(py_exem_tp_cd.equals(exem_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += exem_list.length;
        putIndex = -1;
        

        /* 저율해지유형코드 one-hot */ 
        for(int i=0;i<lwrt_list.length;i++){
            if(lwrt_tmn_rfd_tp_cd.equals(lwrt_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += lwrt_list.length;
        putIndex = -1;


        /* 계약의 보험기간/납입기간 */ 
        input.putScalar(0, curIndex++, ctr_py_prd / 100.0);
        input.putScalar(0, curIndex++, ctr_ins_prd / 100.0);
        // 정확도 향상을 위한 BigDecimal 테스트해봤는데 단순변환으로는 개선 없었음
        //input.putScalar(0, curIndex++, ctr_ins_prd.divide(BigDecimal.valueOf(100)).doubleValue());


        /* 수수료지급유형 one-hot */ 
        for(int i=0;i<fee_list.length;i++){
            if(fee_pay_tp_cd.equals(fee_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += fee_list.length;
        putIndex = -1;


        /* 모집조직 one-hot */ 
        for(int i=0;i<bch_list.length;i++){
            if(rcrt_bch_org_cd.equals(bch_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += bch_list.length;
        putIndex = -1;


        /* 연령 */
        input.putScalar(0, curIndex++, sbc_age / 100.0);


        /* 성별 one-hot */
        if(gndr_cd.equals("1")){
            input.putScalar(0, curIndex, 1);
        }
        else if(gndr_cd.equals("2")){
            input.putScalar(0, curIndex+1, 1);
        }

        curIndex += 2;


        /* 직업급수 one-hot */
        if (injr_gr_num >= 1 && injr_gr_num <= 3){
            input.putScalar(0, curIndex + injr_gr_num - 1, 1);
        }

        curIndex += 3;


        /* 플랜코드 one-hot */
        for(int i=0;i<pl_list.length;i++){
            if(plan_cd.equals(pl_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += pl_list.length;
        putIndex = -1;


        /* 상해등급 one-hot */
        /* 상해등급의 경우, 주어지지 않으면 4종류 다 계산하는게 요건 */
        if(inspe_grde_val.charAt(0) == '1'){
            input.putScalar(0, curIndex + 0, 1);
        }
        else if(inspe_grde_val.charAt(0) == '2'){
            input.putScalar(0, curIndex + 1, 1);
        }
        else if(inspe_grde_val.charAt(0) == '3'){
            input.putScalar(0, curIndex + 2, 1);
        }

        curIndex += 3;


        /* 담보코드 one-hot */ 
        for(int i=0;i<cov_list1.length;i++){
            if(cov_cd.equals(cov_list1[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += cov_list1.length;


        /* 담보코드 one-hot-like */
        double tempInputVal = 0;

        if(putIndex != -1){
            if(cov_list2[putIndex][0] <= 0){
                tempInputVal = 1;
            }
            else if(sbc_amt >= 0){
                tempInputVal = Math.min(1, sbc_amt / cov_list2[putIndex][0]);
            }
            else{
                tempInputVal = cov_list2[putIndex][1] / cov_list2[putIndex][0];
            }

            input.putScalar(0, curIndex + putIndex, tempInputVal);
        }

        curIndex += cov_list1.length;
        putIndex = -1;
        

        /* 나이/기간 등 [0,1]로 스케일링 */
        input.putScalar(0, curIndex++, ins_prd / 100.0);
        input.putScalar(0, curIndex++, py_prd / 100.0);
        input.putScalar(0, curIndex++, rnwl_ed_age / 100.0);
        

        /* 마지막 인덱스 체크 */
        System.out.println("curIndex = " + curIndex);


        return input;

    }


    /* matrix로 한번에 찍어보는 예제 */

    /* 담보코드 한번에 만들어 붙이기 */
    /* 일단 대표상품코드 60546 을 예시로 만들어봄 */
    /* rps_pd_cd 수만큼 맵 만들어야할듯 */
    public static String[] pd_cov_list = 
        {"620255", "620256", "620257", "620258", "620259", "620260", "620264", "620265", "620266"};

    public static INDArray makeInputAllSample(
            /* 계약 정보 */
            String rps_pd_cd, String py_exem_tp_cd, String lwrt_tmn_rfd_tp_cd, 
            int ctr_ins_prd, int ctr_py_prd, String fee_pay_tp_cd, String rcrt_bch_org_cd,
            /* 목적물 정보 */
            int sbc_age, String gndr_cd, int injr_gr_num, String plan_cd, String inspe_grde_val
            ){

        INDArray inputAll, inputDuplicate;

        INDArray input;
        int curIndex = 0;
        int putIndex = -1;

        String[] pd_list = ModelInfo.pd_list;
        String[] exem_list = ModelInfo.exem_list;
        String[] lwrt_list = ModelInfo.lwrt_list;
        String[] fee_list = ModelInfo.fee_list;
        String[] bch_list = ModelInfo.bch_list;
        String[] pl_list = ModelInfo.pl_list;
        String[] cov_list1 = ModelInfo.cov_list1;
        double[][] cov_list2 = ModelInfo.cov_list2;


        /* (담보수) x (계약/피보정보 컬럼수) matrix 생성 */
        inputDuplicate = Nd4j.zeros(pd_cov_list.length, ModelInfo.common_part_len);

        /* 계약/피보정보로 한 줄 만들기 시작 */ 
        input = Nd4j.zeros(1, ModelInfo.common_part_len);

        /* 상품코드 one-hot */
        for(int i=0;i<pd_list.length;i++){
            if(rps_pd_cd.equals(pd_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += pd_list.length;
        putIndex = -1;


        /* 납입면제유형코드 one-hot */ 
        for(int i=0;i<exem_list.length;i++){
            if(py_exem_tp_cd.equals(exem_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += exem_list.length;
        putIndex = -1;
        

        /* 저율해지유형코드 one-hot */ 
        for(int i=0;i<lwrt_list.length;i++){
            if(lwrt_tmn_rfd_tp_cd.equals(lwrt_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += lwrt_list.length;
        putIndex = -1;


        /* 계약의 보험기간/납입기간 */ 
        input.putScalar(0, curIndex++, ctr_py_prd / 100.0);
        input.putScalar(0, curIndex++, ctr_ins_prd / 100.0);
        // 정확도 향상을 위한 BigDecimal 테스트해봤는데 단순변환으로는 개선 없었음
        //input.putScalar(0, curIndex++, ctr_ins_prd.divide(BigDecimal.valueOf(100)).doubleValue());


        /* 수수료지급유형 one-hot */ 
        for(int i=0;i<fee_list.length;i++){
            if(fee_pay_tp_cd.equals(fee_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += fee_list.length;
        putIndex = -1;


        /* 모집조직 one-hot */ 
        for(int i=0;i<bch_list.length;i++){
            if(rcrt_bch_org_cd.equals(bch_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += bch_list.length;
        putIndex = -1;


        /* 연령 */
        input.putScalar(0, curIndex++, sbc_age / 100.0);


        /* 성별 one-hot */
        if(gndr_cd.equals("1")){
            input.putScalar(0, curIndex, 1);
        }
        else if(gndr_cd.equals("2")){
            input.putScalar(0, curIndex+1, 1);
        }

        curIndex += 2;


        /* 직업급수 one-hot */
        if (injr_gr_num >= 1 && injr_gr_num <= 3){
            input.putScalar(0, curIndex + injr_gr_num - 1, 1);
        }

        curIndex += 3;


        /* 플랜코드 one-hot */
        for(int i=0;i<pl_list.length;i++){
            if(plan_cd.equals(pl_list[i])){
                putIndex = i;
                break;
            }
        }

        if(putIndex != -1){
            input.putScalar(0, curIndex + putIndex, 1);
        }
        curIndex += pl_list.length;
        putIndex = -1;


        /* 상해등급 one-hot */
        /* 상해등급의 경우, 주어지지 않으면 4종류 다 계산하는게 요건 */
        if(inspe_grde_val.charAt(0) == '1'){
            input.putScalar(0, curIndex + 0, 1);
        }
        else if(inspe_grde_val.charAt(0) == '2'){
            input.putScalar(0, curIndex + 1, 1);
        }
        else if(inspe_grde_val.charAt(0) == '3'){
            input.putScalar(0, curIndex + 2, 1);
        }

        curIndex += 3;


        /* 계약/피보 정보는 모든 담보에 대해 같으므로, 담보수만큼 복사함 */
        for(int i=0;i<pd_cov_list.length;i++){
            inputDuplicate.putRow(i, input);
        }

        /* 담보코드 관련 matrix는 아래 함수로 만들어와서 붙임 */
        inputAll = Nd4j.concat(1, inputDuplicate, makeCovInput("60546"));

        /* 담보별 ins_prd, py_prd, rnwl_ed_age 는 어떻게 구해와야할지 아직 모르겠음 */ 
        /* 일단 임시로 1년, 1년, 0 으로 하드코딩 세팅 */
        inputAll = Nd4j.concat(1, inputAll, makeCovDetailInput("60546"));

        return inputAll;
    }


    public static INDArray makeCovInput(String rps_pd_cd){
        
        INDArray covInput;
        String[] cov_list1 = ModelInfo.cov_list1;
        double[][] cov_list2 = ModelInfo.cov_list2;
        int putIndex = -1;

        covInput = Nd4j.zeros(pd_cov_list.length, cov_list1.length*2);


        for(int covIndex=0;covIndex<pd_cov_list.length;covIndex++){

            putIndex = -1;

            /* 담보코드 one-hot */ 
            for(int i=0;i<cov_list1.length;i++){
                if(pd_cov_list[covIndex].equals(cov_list1[i])){
                    putIndex = i;
                    break;
                }
            }

            if(putIndex != -1){
                covInput.putScalar(covIndex, putIndex, 1);
            }

            /* 담보코드 one-hot-like */
            if(putIndex != -1){
                covInput.putScalar(covIndex, cov_list1.length + putIndex, cov_list2[putIndex][1] / cov_list2[putIndex][0]);
            }

        }

        return covInput;

    }

    public static INDArray makeCovDetailInput(String rps_pd_cd){
        
        INDArray covDetailInput;

        covDetailInput = Nd4j.zeros(pd_cov_list.length, 3);

        for(int i=0;i<pd_cov_list.length;i++){
            covDetailInput.putScalar(i, 0, 1/100.0);
            covDetailInput.putScalar(i, 1, 1/100.0);
            covDetailInput.putScalar(i, 2, 0/100.0);
        }

        return covDetailInput;

    }

    public static void showINDArray(INDArray array){

        double scalarVal = 0;

        System.out.println("--------------showINDArray--------------");
        System.out.println("INDArray length: " + array.rows() + ", " + array.columns());

        //for(int i=0;i<array.length();i++){
        for(int i=0;i<array.rows();i++){
            for(int j=0;j<array.columns();j++){
                scalarVal = array.getDouble(i, j);
                if(scalarVal != 0){
                    System.out.println("INDArray index = "+i+", "+j+" : "+scalarVal);
                }
            }
            System.out.println("----------------------------------------");
        }

    }


}
