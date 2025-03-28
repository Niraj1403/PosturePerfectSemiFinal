import * as tf from '@tensorflow/tfjs';
import { loadSuryaNamaskarModel } from "../../tensorflow/suryaNamaskarModel";

let suryaModel;



export async function loadSuryaNamaskarModel() {
    if (!suryaModel) {  // ✅ Prevents reloading
        suryaModel = await tf.loadGraphModel('/models/surya/surya_model.json');
        console.log("🟠 Surya Namaskar Model Loaded");
    }
}

export function getSuryaNamaskarModel() {
    return suryaModel;
}
